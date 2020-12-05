from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from watcher.models import *
from .serializers import *
import requests
import json
from django.db.models import Q
from django.shortcuts import redirect,render

def get_client_store_list(request) :
	pages = request.GET.get('page',0)
	keyword = request.GET.get('search_keyword',"None")

	print(pages)
	if keyword == "None" :
		stores = Store.objects.all()
	else :
		stores = Store.objects.filter( Q(store_name__icontains=keyword) | Q(store_location__icontains=keyword))

	paginator = Paginator(stores,5)

	try :
		stores = paginator.page(pages)
	except PageNotAnInteger :
		stores = paginator.page(0)
	except EmptyPage :
		stores = paginator.page(paginator.num_pages)
		data = {
			'msg' : "end",
		}
		return JsonResponse(data)

	serialized_stores = StoreSerializer(stores,many=True)
	pages = int(pages) +int(1)
	data ={
		'st' : serialized_stores.data,
		'page' : pages,
		'msg' : "good",
	}

	return JsonResponse(data)


def search_client_store_list(request) :
	keyword = request.GET['search_keyword']

	stores = Store.objects.filter( Q(store_name__icontains=keyword) | Q(store_location__icontains=keyword))
	paginator = Paginator(stores,5)
	pages = request.GET.get('page_search',1)

	try :
		stores = paginator.page(pages)
	except PageNotAnInteger :
		stores = paginator.page(1)
	except EmptyPage :
		stores = paginator.page(paginator.num_pages)
		return HttpResponse("end")

	serialized_stores = StoreSerializer(stores,many=True)

	return HttpResponse(json.dumps(serialized_stores.data))


def client_liked_list(request) :
	pk_list = request.GET.getlist('pk_list[]','')
	stores = Store.objects.none()

	if pk_list :
		for pk in pk_list :
			stores = stores | Store.objects.filter(pk=pk)
		serialized_stores = StoreSerializer(stores,many=True)
		return HttpResponse(json.dumps(serialized_stores.data))
	else :
		return HttpResponse("None")


def client_signin(request) :
	user_id=request.POST.get('user_id')
	password=request.POST.get('password')

	user=User.objects.filter(Q(user_id=user_id) & Q(password=password))

	if user.exists() :
		request.session['user_id']=user_id
		return HttpResponse("good")
	else :
		return HttpResponse("loginfail")

	

def client_signup(request) :
	user_id=request.POST.get('user_id')
	password=request.POST.get('password')
	password_check=request.POST.get('password_check')

	user=User.objects.filter(user_id=user_id)

	if user.exists() :
		return HttpResponse("sameid")
	request.session['user_id']=user_id

	user=User(user_id=user_id,password=password)
	user.save()
	return HttpResponse("signup")

def client_logout(requset) :
	requset.session.clear()
	return HttpResponse("good")





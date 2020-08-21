from django.http import HttpResponse, JsonResponse
from watcher.models import *
import json

def get_camera_list(request):
	pk = int(request.GET['pk'])
	camera_info = Camera.objects.get(pk=pk)

	output = {
		'elec_avaliable' : camera.elec_available
	} 


	return JsonResponse(data, safe=False)

def get_store_list(request) :
	pk = int(request.GET['pk'])
	store_info = Store.objects.get(pk=pk)

	data = {
		'pk' : store_info.pk,
		'store_name' : store_info.store_name,
		'store_loaction' : store_info.store_loaction,
	}

	return JsonResponse(data, safe=False)


def add_store_list(request) :
	store_name = request.GET['store_name']
	store_location = request.GET['store_location']

	store = Store(store_name = store_name, store_location = store_location)
	store.save()

	store_list = Store.objects.all()
	return render(request, 'watcher/store_list.html',{"store_list" : store_list})


def send_store_pk(requset) :
	store_id = requset.GET['store_id']

	return render(requset, 'watcher/Camers_list.html',{"store_id" : store_id})

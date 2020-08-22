from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from watcher.models import *
from django.views.decorators.csrf import csrf_exempt
from watcher.tools import *

# Create your views here.
def Camera_list(request,store_id) :
	camera_list = Camera.objects.filter(store_id = store_id)
	return render(request, 'watcher/Camera_list.html',{"camera_list": camera_list, "store_id" : store_id } )

def table_set(request):
	return render(request, 'watcher/table_set_fabric.html')

def store_list(request) :
	store_list = Store.objects.all()
	return render(request, 'watcher/store_list.html',{"store_list" : store_list})

@csrf_exempt
def image_test(request):
	handle_uploaded_file(request.FILES['file'])


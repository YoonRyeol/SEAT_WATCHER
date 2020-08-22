from django.http import HttpResponse, JsonResponse
from watcher.models import *
import json
from django.shortcuts import render

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

def get_camera_list(request):
	pk = int(request.GET['pk'])
	camera = Camera.objects.get(pk=pk)

	output = {
		'pk' : camera.pk,
		'store_id' : camera.store_id,
		'cur_pic' : cur_pic,
		'mac_addr' : mac_addr,
		'cur_host' : cur_host,
		'description' : description,
	} 


	return JsonResponse(data, safe=False)

def add_camera_list(request) :
	cur_pic = request.GET['cur_pic']
	description = request.GET['description']
	store_id= int(request.GET['store_id'])

	camera=Camera(cur_pic=cur_pic, description = description, mac_addr="ddd", cur_host="cur_host",store_id = store_id)
	camera.save()

	camera_list = Camera.objects.filter(store_id = store_id)
	return render(request, 'watcher/Camera_list.html',{"camera_list" : camera_list})


def delete_camera_list(request) :

	store_id = int(request.GET['store_id'])
	pk = int(request.GET['pk'])

	camera = Camera.objects.filter(pk=pk, store_id= store_id)
	camera.delete()

	camera_list = Camera.objects.filter(store_id = store_id)
	return render(request, 'watcher/Camera_list.html',{"camera_list" : camera_list})


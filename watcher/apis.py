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
		'store_location' : store_info.store_location,
	}

	return JsonResponse(data, safe=False)


def add_store_list(request) :
	store_name = request.GET['store_name']
	store_location = request.GET['store_location']

	store = Store(store_name = store_name, store_location = store_location)
	store.save()
	

	data = {
		'pk' : store.pk,
		'store_name' : store.store_name,
		'store_location' : store.store_location,
	}

	return JsonResponse(data, safe=False)


def get_camera_info(request):
	pk = int(request.GET['pk'])
	camera = Camera.objects.get(pk=pk)

	data = {
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

	camera=Camera(cur_pic=cur_pic, description = description, cur_host="cur_host",store_id = store_id)
	camera.save()

	data = {
		'pk' : camera.pk,
		'store_id' : camera.store_id,
		'cur_pic' : camera.cur_pic,
		'mac_addr' : camera.mac_addr,
		'cur_host' : camera.cur_host,
		'description' : camera.description,

	}
	return JsonResponse(data, safe=False)


def delete_camera_list(request) :

	store_id = int(request.GET['store_id'])
	pk = int(request.GET['pk'])

	camera = Camera.objects.filter(pk=pk, store_id= store_id)
	camera.delete()

	camera_list = Camera.objects.filter(store_id = store_id)
	camera = camera_list.first();

	data = {
		'pk' : camera.pk,
		'store_id' : camera.store_id,
		'cur_pic' : camera.cur_pic,
		'mac_addr' : camera.mac_addr,
		'cur_host' : camera.cur_host,
		'description' : camera.description,

	}
	return JsonResponse(data, safe=False)


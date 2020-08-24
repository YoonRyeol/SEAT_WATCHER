from django.http import JsonResponse, HttpResponse
from watcher.models import *
import requests
import json
from watcher.tools import *
import os
from django.utils import timezone
from django.shortcuts import render
from django.core import serializers


def send_seat_data(request):
	"""
	Todo : get camera id, store id
	"""
	before_pk_list = json.loads(request.POST['before_pk_list'])

	string_data = request.POST['seat_data']
	camera_pk = int(request.POST['camera_pk'])
	camera = Camera.objects.get(pk=camera_pk)
	store_pk = int(request.POST['store_pk'])
	store = Store.objects.get(pk=store_pk)
	real_data = json.loads(string_data)
	"""
	real data format
	{
		'is_elec': False, 
		'capacity': '1', 
		'position': {'f_x': 0.19416666666666665, 'f_y': 0.35, 's_x': 0.2808333333333333, 's_y': 0.46555555555555556}
	}
	"""

	"""
	Todo : cam addr setting : connection test
	"""
	cam_host = camera.cur_host
	cam_addr_test = '/'.join([cam_host, 'test'])

	try:
		response = requests.get(cam_addr_test, timeout=5)
	except Exception:
		return HttpResponse('connection error')
	if response.text != 'ok':
		return HttpResponse('connection error2')
	
	cur_pk_list = []

	to_cam_data_list = []

	for elem in real_data:
		to_cam_data = {}

		target_data = {
			'pic_f_x' : elem['position']['f_x'],
			'pic_f_y' : elem['position']['f_y'],
			'pic_s_x' : elem['position']['s_x'],
			'pic_s_y' : elem['position']['s_y'],
			'is_elec' : elem['is_elec'],
			'capacity' : elem['capacity'],
			'camera' : camera,
			'store' : store,
		}
		if bool(elem['pk']):
			cur_pk_list.append(elem['pk'])
			Table.objects.filter(pk=elem['pk']).update(**target_data)
			to_cam_data['pk'] = elem['pk']
			to_cam_data['position'] = elem['position']
			to_cam_data_list.append(to_cam_data)
		else:
			table_tmp = Table.objects.create(**target_data)
			to_cam_data['pk'] = table_tmp.pk
			to_cam_data['position'] = elem['position']
			to_cam_data_list.append(to_cam_data)

	"""
	Todo : table delete
	"""
	for before_pk in before_pk_list:
		if before_pk not in cur_pk_list:
			Table.objects.filter(pk=before_pk).delete()
	
	"""
	send coord to cam
	"""
	cam_get_seat_info = '/'.join([camera.cur_host, 'get_seat_info'])
	try:
		response = requests.post(cam_get_seat_info, data={'seat_data':json.dumps(to_cam_data_list)}, timeout=5)
	except Exception:
		return HttpResponse('connection error')
	if response.text != 'good':
		return HttpResponse('connection error2')

	return HttpResponse('good')


#가게 정보 관련 
def get_store_info(request) :
	pk = int(request.GET['pk'])
	store_info = Store.objects.get(pk=pk)

	data = {
		'pk' : store_info.pk,
		'store_name' : store_info.store_name,
		'store_location' : store_info.store_location,
	}

	return JsonResponse(json.dumps(store_info))


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

#카메라 정보 관련

def get_camera_info(request):
	pk = int(request.GET['pk'])
	camera = Camera.objects.get(pk=pk)

	data = {
		'pk' : camera.pk,
		'store_id' : camera.store_id,
		'cur_pic' : camera.cur_pic,
		'mac_addr' : camera.mac_addr,
		'cur_host' : camera.cur_host,
		'description' : camera.description,
	} 
	return JsonResponse(data, safe=False)

def add_camera_list(request) :
	cur_pic = request.GET['cur_pic']
	description = request.GET['description']
	store_id= int(request.GET['store_id'])
	camera=Camera(cur_pic=cur_pic, description = description, store_id = store_id)
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

def get_camera_info_without_floor(request) :
	store_id = int(request.GET['store_id'])
	camera_floor_list = Camera.objects.filter(store_id= store_id, floor_id__isnull= True)

	camera = camera_floor_list.first();

	data = serializers.serialize("json",camera_floor_list,fields=('id','cur_pic','description','mac_addr','cur_host','store_id','floor_id'))
	
	return HttpResponse(data)

def delete_camera_list(request) :

	store_id = int(request.GET['store_id'])
	pk = int(request.GET['pk'])

	camera = Camera.objects.filter(pk=pk, store_id= store_id)
	camera.delete()

	camera_list = Camera.objects.filter(store_id = store_id)
	camera = camera_list.first()

	data = {
		'pk' : camera.pk,
		'store_id' : camera.store_id,
		'cur_pic' : camera.cur_pic,
		'mac_addr' : camera.mac_addr,
		'cur_host' : camera.cur_host,
		'description' : camera.description,

	}
	return JsonResponse(data, safe=False) #수정 필요

#층 정보 관련
def add_floor_info(request) :

	store_id = int(request.GET['store_id'])
	floor_num = int(request.GET['floor_num'])
	floor_name = request.GET['floor_name']
	description = request.GET['description']
	camera_list = request.GET.getlist('camera_list[]')


	floor=Floor(store_id=store_id, floor_num=floor_num, name=floor_name,description=description)
	floor.save()

	for c_list in camera_list :
		camera = Camera.objects.filter(pk=int(c_list))
		camera.update(floor_id=floor.pk)

	c_list = Camera.objects.filter(floor_id = floor.pk)

	data = {
		'pk' : floor.pk,
		'floor_num' : floor.floor_num,
		'name' : floor.name,
		'description' : floor.description,
	}
	return JsonResponse(data, serializers('json',c_list))


def test(request) :


	camera_list = request.GET.getlist('camera_list[]')
	floor_id = int(request.GET['floor_pk'])

	for c_list in camera_list :
		camera = Camera.objects.filter(pk=int(c_list))
		camera.update(floor_id=int(8))


	ß
	return HttpResponse("good");

def get_file_from_cam(request):
	"""
	Todo : 카메라 pk, 가게 pk -> 카메라에 cur_pic 이름 저장
	"""
	cur_host = request.POST['host_addr']
	target_addr = '/'.join([cur_host, 'send_image'])
	response = requests.get(target_addr, stream=True)
	if response.status_code == 200:
		with open('watcher/static/img/test.jpg', 'wb') as f:
			for chunk in response:
				f.write(chunk)
	return HttpResponse('/static/img/test.jpg')

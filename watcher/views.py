from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from watcher.models import *
from django.views.decorators.csrf import csrf_exempt
from watcher.tools import *
from django.forms.models import model_to_dict
import json

# Create your views here.
def Camera_list(request,store_id) :
	camera_list = Camera.objects.filter(store_id = store_id)
	store = Store.objects.get(pk = store_id)
	floor_list = Floor.objects.filter(store_id = store_id)
	return render(request, 'watcher/Camera_list.html',{"camera_list": camera_list, "store" : store ,"floor_list" : floor_list,} )

def table_set(request, store_pk=None, camera_pk=None):
	store = Store.objects.get(pk=store_pk)
	camera = Camera.objects.get(pk=camera_pk)
	"""
	Todo : 사진 데이터 로드
	"""
	if bool(camera.cur_pic):
		picture_name = camera.cur_pic
	else:
		picture_name = 'no_image.jpg'
	"""
	Todo : 좌석데이터 로드
	"""
	table_tmp = Table.objects.filter(camera=camera)
	table_list = []
	for e in table_tmp:
		table_list.append(model_to_dict(e))

	return render(request, 'watcher/table_set_fabric.html', {
																'table_list': json.dumps(table_list),
																'picture_name' : picture_name,
																'store_pk' : store_pk,
																'camera_pk' : camera_pk,
																'cam_cur_host' : camera.cur_host
																									})
def store_layout(request, store_pk=None, floor_pk=None):
	camera_list = Camera.objects.filter(store__pk=store_pk, floor__pk=floor_pk)
	data_list=[]
	for camera in camera_list:
		undeployed_table_list = Table.objects.filter(camera=camera, layout_f_x=None)
		deployed_table_list = Table.objects.filter(camera=camera).exclude(layout_f_x=None)
		datum = {
			'camera':camera,
			'undeployed_table_list' : undeployed_table_list,
			'deployed_table_list' : deployed_table_list
		}
		data_list.append(datum)
	table_tmp = Table.objects.filter(store__pk=store_pk, floor__pk=floor_pk).exclude(layout_f_x=None)
	table_list = []
	for e in table_tmp:
		table_list.append(model_to_dict(e))
	return render(request, 'watcher/store_layout.html', {
															'table_list':json.dumps(table_list),
															'data_list':data_list,
															'floor_pk' : floor_pk,
																								})


def cam_picture(request, camera_pk):
	camera = Camera.objects.get(pk=camera_pk)
	"""
	Todo : 사진 데이터 로드
	"""
	if bool(camera.cur_pic):
		picture_name = camera.cur_pic
	else:
		picture_name = 'no_image.jpg'
	"""
	Todo : 좌석데이터 로드
	"""
	table_tmp = Table.objects.filter(camera=camera)
	table_list = []
	for e in table_tmp:
		table_list.append(model_to_dict(e))

	return render(request, 'watcher/cam_picture.html', {
														'picture_name' : picture_name,
														'table_list' : json.dumps(table_list)
																						})

def store_list(request) :
	store_list = Store.objects.all()
	return render(request, 'watcher/store_list.html',{"store_list" : store_list})

def client_store_list(request) :
	store_list = Store.objects.all()
	return render(request, 'watcher/client_store_list.html',{"store_list" : store_list})

def client_page(request, store_pk=None):
	store = None
	if store_pk != None:
		store = Store.objects.get(pk=int(store_pk))
	all_table_count = Table.objects.filter(store__pk=store_pk).count()
	occupied_table_count = Table.objects.filter(store__pk=store_pk, is_occupied=True).count()
	elec_all = Table.objects.filter(store__pk=store_pk, is_elec=True).count()
	elec_occupied = Table.objects.filter(store__pk=store_pk, is_elec=True, is_occupied=True).count()
	floor_list = Floor.objects.filter(store__pk = store_pk)

	layout_coord_list = []

	for floor in floor_list:
		table_list = Table.objects.filter(floor=floor)
		tmp_list = []
		for e in table_list:
			tmp_list.append(model_to_dict(e))
		tmp_data = {
			'floor' : model_to_dict(floor),
			'coor_list' : tmp_list
		}
		layout_coord_list.append(tmp_data)



	return render(request, 'watcher/client_page.html', {
														'store' : store,
														'all_table_count':all_table_count,
														'occupied_table_count':occupied_table_count,
														'floor_list' : floor_list,
														'elec_all':elec_all,
														'elec_occupied':elec_occupied,
														'layout_coord_list' : json.dumps(layout_coord_list),
																									})

@csrf_exempt
def image_test(request):

	handle_uploaded_file(request.FILES['file'])


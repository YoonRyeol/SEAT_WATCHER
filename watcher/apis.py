from django.http import JsonResponse, HttpResponse, FileResponse
from watcher.models import *
import requests
import json
from watcher.tools import *
import os
from django.utils import timezone
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .serializers import *
from rest_framework.response import Response
from django.core.files.storage import default_storage #파일 저장 경로
from google.cloud import vision
from django.conf import settings
import traceback

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
	picture_name = request.POST['picture_name']
	real_data = json.loads(string_data)
	"""
	camera data set
	"""
	Camera.objects.filter(pk=camera_pk).update(cur_pic=picture_name)
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
			'pic_f_x' : round(elem['position']['f_x'],2),
			'pic_f_y' : round(elem['position']['f_y'],2),
			'pic_s_x' : round(elem['position']['s_x'],2),
			'pic_s_y' : round(elem['position']['s_y'],2),
			'is_elec' : elem['is_elec'],
			'capacity' : elem['capacity'],
			'camera' : camera,
			'store' : store,
			'pic_name': picture_name,
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
		output_data = {
			'is_updated' : True,
			'data' : to_cam_data_list
		}
		response = requests.post(cam_get_seat_info, data={'seat_data':json.dumps(output_data, indent=4)}, timeout=5)
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
def delete_store_info(request) :
	pk = int(request.GET['pk'])
	store = Store.objects.get(pk=pk)
	store.delete()
	return HttpResponse("delete success")

def edit_store_info(request) :
	pk = int(request.POST.get('pk'))
	store_name = request.POST['store_name']
	store_location = request.POST.get('store_location')
	picture_name = request.POST.get('picture_name')
	pic = request.FILES.get('img')

	store = Store.objects.get(pk=pk)
	
	if pic :
		default_storage.delete('watcher/static/img/store/'+str(pk)+'/'+store.picture_name)
		default_storage.save('watcher/static/img/store/'+str(pk)+'/'+pic.name, pic)

	store.store_name = store_name
	store.store_location = store_location
	store.picture_name = picture_name
	store.save()

	stores = Store.objects.all()
	serialized_stores = StoreSerializer(stores,many=True)

	return HttpResponse(json.dumps(serialized_stores.data))

def add_store_list(request) :
	store_name = request.POST.get('store_name')
	store_location = request.POST.get('store_location')
	picture_name = request.POST.get('picture_name',"modal_cafe_img.jpg")
	pic = request.FILES.get('img')
		
	store = Store(store_name=store_name, store_location=store_location, picture_name=picture_name)
	store.save()

	if pic :
		default_storage.save('watcher/media/img/store/'+str(store.pk)+'/'+pic.name, pic)
		store.picture_name=pic.name
		store.save()
	
	data = {
		'pk' : store.pk,
		'store_name' : store.store_name,
		'store_location' : store.store_location,
		'picture_name' : store.picture_name,
	}

	return JsonResponse(data, safe=False)

def upload_store_img(requset) :
	picture_name = requset.GET.get('picture_name')
	print("img_start")
	return HttpResponse('img good')



#카메라 정보 관련

def get_camera_info(request):
	pk = int(request.POST.get('pk'))
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

def edit_camera_info(request) :
	store_id = int(request.GET['store_id'])
	pk = int(request.GET['pk'])
	mac_addr = request.GET.get('mac_addr')
	description = request.GET['description']
	cur_host = request.GET.get('cur_host')

	camera = Camera.objects.filter(pk=pk)
	camera.update(mac_addr=mac_addr,description=description,cur_host=cur_host)
	camera = Camera.objects.get(pk=pk)

	cameras = Camera.objects.filter(store_id=store_id)
	serialized_cameras = CameraSerializer(cameras,many=True)

	return HttpResponse(json.dumps(serialized_cameras.data))
	
def add_camera_info(request) :
	#cur_pic = request.GET['cur_pic']
	description = request.GET['description']
	store_id= int(request.GET['store_id'])
	cur_host = request.GET.get('cur_host')
	mac_addr = request.GET.get('mac_addr')


	camera=Camera(description = description, store_id = store_id, cur_host= cur_host, mac_addr=mac_addr)
	camera.save()

	data = {
		'pk' : camera.pk,
		'store_id' : camera.store_id,
		'cur_pic' : camera.cur_pic,
		'mac_addr' : camera.mac_addr,
		'cur_host' : camera.cur_host,
		'description' : camera.description,
		'floor_id' : camera.floor_id,
	}
	return JsonResponse(data, safe=False) 

def get_camera_info_without_floor(request) :
	store_id = int(request.GET['store_id'])
	camera_floor_list = Camera.objects.filter(store_id= store_id, floor_id__isnull= True)
	camera = camera_floor_list.first()

	data = serializers.serialize("json",camera_floor_list,fields=('id','cur_pic','description','mac_addr','cur_host','store_id','floor_id'))
	
	return HttpResponse(data)

def delete_camera_list(request) :

	store_id = int(request.GET['store_id'])
	pk = int(request.GET['pk'])

	camera = Camera.objects.filter(pk=pk, store_id= store_id)
	camera.delete()

	
	return HttpResponse('delete success') #수정 필요 -> 2020-08-25 수정완료

def check_camera_connection(request) :
	cur_host = request.POST.get('cur_host')

	try :
		rq = requests.get(cur_host+'/test',timeout=5)
		if rq.text != 'ok' :
			return HttpResponse('bad')
	except Exception as e :
		return HttpResponse('bad')


def check_camera_connection_table(request) :
	cur_host = request.POST.get('cur_host')
	pk = int(request.POST['pk'])

	try :
		rq = requests.get(cur_host+'/test',timeout=5)
		if rq.text != 'ok' :
			data = {
				'pk' : pk,
				'con' : "bad",
			}
		else:
			data = {
				'pk' : pk,
				'con' : 'good'
			}
		return JsonResponse(data)
	except Exception as e :
		data = {
			'pk' :pk,
			'con' : "bad",
		}
		return JsonResponse(data)


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

	data = {
		'pk' : floor.pk,
		'floor_num' : floor_num,
		'name' : floor.name,
		'description' : floor.description,
	}
	return JsonResponse(data)


def edit_floor_id(request) :

	camera_list = request.POST.getlist('camera_list[]')
	store_id = int(request.POST.get('store_id'))
	floor_id = int(request.POST.get('floor_id'))

	for c_list in camera_list :
		camera = Camera.objects.filter(pk=int(c_list))
		camera.update(floor_id=floor_id)

	cameras = Camera.objects.filter(store_id=store_id)
	serialized_cameras = CameraSerializer(cameras,many=True)

	return HttpResponse(json.dumps(serialized_cameras.data))

def delete_floor_info(request) :

	floor_id = int(request.GET['floor_id'])
	store_id = int(request.GET['store_id'])

	floor = Floor.objects.filter(pk=floor_id)
	floor.delete()

	cameras = Camera.objects.filter(store_id=store_id)
	serialized_cameras = CameraSerializer(cameras,many=True)

	return HttpResponse(json.dumps(serialized_cameras.data))

def edit_floor_camera_list(request) :

	camera_used_list = request.GET.getlist('camera_used[]')
	camera_unused_list = request.GET.getlist('camera_unused[]')
	store_id = int(request.GET['store_id'])
	floor_id = int(request.GET['floor_id'])
	name = request.GET['floor_name']
	floor_num = int(request.GET['floor_num'])
	description = request.GET['floor_description']

	floor = Floor.objects.filter(pk=floor_id)
	floor.update(name=name,floor_num=floor_num,description=description)

	for lists in camera_used_list :
		camera = Camera.objects.filter(pk=int(lists))
		camera.update(floor_id=floor_id)

	for lists in camera_unused_list :
		camera = Camera.objects.filter(pk=int(lists))
		camera.update(floor_id=None)

	cameras = Camera.objects.filter(store_id=store_id)

	serialized_cameras = CameraSerializer(cameras,many=True)
	return HttpResponse(json.dumps(serialized_cameras.data)) 



def get_file_from_cam(request):
	"""
	Todo : 카메라 pk, 가게 pk -> 카메라에 cur_pic 이름 저장
	"""
	cur_time = timezone.now().strftime("%Y%m%d%H%M%S")
	camera_pk = request.POST['camera_pk']
	cur_host = request.POST['host_addr']
	target_addr = '/'.join([cur_host, 'send_image'])
	cur_pic_name = cur_time+str(camera_pk)
	response = requests.get(target_addr, stream=True)
	if response.status_code == 200:
		with open('watcher/static/img/'+cur_pic_name+'.jpg', 'wb') as f:
			for chunk in response:
				f.write(chunk)
	
	return JsonResponse({
		'path' : '/static/img/'+ cur_pic_name + '.jpg',
		'pic_name' : cur_pic_name + '.jpg'
	})


def save_layout(request):
	layout_pos_data = json.loads(request.POST['layout_pos_data'])
	before_pk_list = json.loads(request.POST['before_pk_list'])
	floor_pk = int(request.POST['floor_pk'])
	floor = Floor.objects.get(pk=floor_pk)
	cur_pk_list = []
	for datum in layout_pos_data:
		save_datum = {
			'floor':floor,
			'layout_f_x':datum['f_x'],
			'layout_f_y':datum['f_y'],
			'layout_s_x':datum['s_x'],
			'layout_s_y':datum['s_y']
		}
		Table.objects.filter(pk=int(datum['pk'])).update(**save_datum)
		cur_pk_list.append(datum['pk'])

	
	for before_pk in before_pk_list:

		if before_pk not in cur_pk_list:
			save_datum = {
				'floor':None,
				'layout_f_x':None,
				'layout_f_y':None,
				'layout_s_x':None,
				'layout_s_y':None
			}
			Table.objects.filter(pk=before_pk).update(**save_datum)

	return HttpResponse('good')

@csrf_exempt
def get_seat_inspection_result(request):
	inspection_result = json.loads(request.POST['input'])
	for e in inspection_result:
		is_occupied = None
		if e['res'] == 'T':
			is_occupied = True
		else:
			is_occupied = False
		Table.objects.filter(pk=e['pk']).update(is_occupied=is_occupied)

	return HttpResponse('good')

def localize_objects(request):
	pic_name = request.POST['pic_name']
	client = vision.ImageAnnotatorClient()
	path = 'watcher/static/img/'+pic_name

	with open(path, 'rb') as image_file:
		content = image_file.read()
	image = vision.types.Image(content=content)
    
	objects = client.object_localization(image=image).localized_object_annotations

	output_data = []

	target_data = ['Table', 'Tableware']

	for object_ in objects:
		if object_.name in target_data:
			vertex_list = object_.bounding_poly.normalized_vertices
			data = {
				'x' : vertex_list[0].x,
				'y' : vertex_list[0].y,
				'width' : abs(vertex_list[0].x - vertex_list[1].x),
				'height' : abs(vertex_list[0].y - vertex_list[3].y)
			}
			output_data.append(data)
	
	return HttpResponse(json.dumps(output_data))

def update_cam_addr(request):
	camera_pk = int(request.POST['camera_pk'])
	camera = Camera.objects.get(pk=camera_pk)
	camera_mac_addr = camera.mac_addr

	if bool(camera_mac_addr) == False:
		return HttpResponse('camera_mac_addr_failure')

	developerkey =  settings.REMOTE_IT_DEVELOPER_KEY

	headers = {
		'developerkey' : developerkey
	}

	body = {
		'password' : settings.REMOTE_IT_PASSWORD,
		'username' : settings.REMOTE_IT_USERNAME
	}

	url = 'https://api.remot3.it/apv/v27/user/login'

	response = requests.post(url, data=json.dumps(body), headers=headers)
	response_body = response.json()

	if response_body['status'] == 'false':
		return HttpResponse('connection_failure')

	token = response_body['token']

	headers = {
    	"developerkey":developerkey,
	    "token":token
	}

	body = {
    	"deviceaddress": camera_mac_addr,
    	"wait":"true",
	}

	url = "https://api.remot3.it/apv/v27/device/connect"

	response = requests.post(url, data=json.dumps(body), headers=headers)
	response_body = response.json()

	if response_body['status'] == 'false':
		return HttpResponse('addr_update_failure')
	
	camera.cur_host = response_body['connection']['proxy']
	camera.save()

	return HttpResponse('update_success')

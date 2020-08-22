from django.http import JsonResponse, HttpResponse
from watcher.models import *
import requests
import json
from watcher.tools import *
import os
from django.utils import timezone

def send_seat_data(request):
	"""
	Todo : get camera id, store id
	"""
	before_pk_list = json.loads(request.POST['before_pk_list'])

	string_data = request.POST['seat_data']
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
	try:
		response = requests.get('http://localhost:8010/test', timeout=5)
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
			'capacity' : elem['capacity']
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
	try:
		response = requests.post('http://localhost:8010/get_seat_info', data={'seat_data':json.dumps(to_cam_data_list)}, timeout=5)
	except Exception:
		return HttpResponse('connection error')
	if response.text != 'good':
		return HttpResponse('connection error2')

	return HttpResponse('good')

def get_data(request):
	pk = int(request.GET['pk'])
	camera = Camera.objects.get(pk=pk)

	output = {
		'elec_avaliable' : camera.elec_available
	} 

	return HttpResponse(json.dumps(output))

def get_file_from_cam(request):
	"""
	Todo : 카메라 pk, 가게 pk -> 카메라에 cur_pic 이름 저장
	"""
	response = requests.get('http://localhost:8010/send_image', stream=True)
	if response.status_code == 200:
		with open('watcher/static/img/test.jpg', 'wb') as f:
			for chunk in response:
				f.write(chunk)
	return HttpResponse('/static/img/test.jpg')
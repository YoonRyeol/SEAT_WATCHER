from django.http import JsonResponse, HttpResponse
from watcher.models import *
import requests
import json

def send_seat_data(request):
	"""
	Todo : get camera id, store id
	"""
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
	Todo : cam addr setting
	"""
	try:
		response = requests.post('http://localhost:8010/get_seat_info', data={'seat_data':string_data}, timeout=5)
	except Exception:
		return HttpResponse('connection error')
	if response.text != 'good':
		return HttpResponse('connection error2')
	
	for elem in real_data:
		target_data = {
			'pic_f_x' : elem['position']['f_x'],
			'pic_f_y' : elem['position']['f_y'],
			'pic_s_x' : elem['position']['s_x'],
			'pic_s_y' : elem['position']['s_y'],
			'is_elec' : elem['is_elec'],
			'capacity' : elem['capacity']
		}
		Table.objects.create(**target_data)


	return HttpResponse('good')

def get_data(request):
	pk = int(request.GET['pk'])
	camera = Camera.objects.get(pk=pk)

	output = {
		'elec_avaliable' : camera.elec_available
	} 

	return HttpResponse(json.dumps(output))

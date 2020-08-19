from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from watcher.models import *
import json
# Create your views here.


def Get_Camera_list(request) :
	camera_list = Camera.objects.all()
	return render(request, 'watcher/Camera_list.html',{'camera_list' : camera_list})

def get_data(request) :
	pk = int(request.GET['pk'])
	camera_info = Camera.objects.get(pk=pk)

	data = {
		'pk' : camera_info.pk,
		'store_id' : camera_info.store_id,
		'elec_available' : camera_info.elec_available,
	}

	return JsonResponse(data, safe=False)

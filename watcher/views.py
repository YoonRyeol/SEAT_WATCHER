from django.shortcuts import render
from watcher.models import *
# Create your views here.


def Get_Camera_list(request) :
	camera_list = Camera.objects.all()
	return render(request, 'watcher/Camera_list.html',{'camera_list' : camera_list})


def Guest_page(request) :
	return render(request, 'watcher/Guest_page.html')

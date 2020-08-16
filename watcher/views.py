from django.shortcuts import render
from watcher.models import *
# Create your views here.


def Camera_list(request) :
	return render(request, 'watcher/Camera_list.html')


def table_set(request):
	return render(request, 'watcher/table_set_fabric.html')
from django.shortcuts import render
from watcher.models import *
# Create your views here.


def Camera_list(request) :
	return render(request, 'watcher/Camera_list.html')

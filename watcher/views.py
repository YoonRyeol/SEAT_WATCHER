from django.shortcuts import render
from watcher.models import *
from django.views.decorators.csrf import csrf_exempt
from watcher.tools import *

# Create your views here.

def Camera_list(request) :
	return render(request, 'watcher/Camera_list.html')

def table_set(request):
	return render(request, 'watcher/table_set_fabric.html')

@csrf_exempt
def image_test(request):
	handle_uploaded_file(request.FILES['file'])
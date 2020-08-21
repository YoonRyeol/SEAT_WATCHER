from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from watcher.models import *
from django.views.decorators.csrf import csrf_exempt
from watcher.tools import *

# Create your views here.
def Camera_list(request) :
	return render(request, 'watcher/Camera_list.html')

def table_set(request):
	"""
	Todo : 사진 데이터 로드
	"""
	"""
	Todo : 좌석데이터 로드
	"""
	return render(request, 'watcher/table_set_fabric.html')

@csrf_exempt
def image_test(request):
	handle_uploaded_file(request.FILES['file'])


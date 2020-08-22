from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from watcher.models import *
from django.views.decorators.csrf import csrf_exempt
from watcher.tools import *
from django.forms.models import model_to_dict
import json

# Create your views here.
def Camera_list(request) :
	return render(request, 'watcher/Camera_list.html')

def table_set(request, store_pk=None, camera_pk=None):
	"""
	Todo : 사진 데이터 로드
	"""
	"""
	Todo : 좌석데이터 로드
	"""
	table_tmp = Table.objects.all()
	table_list = []
	for e in table_tmp:
		table_list.append(model_to_dict(e))

	return render(request, 'watcher/table_set_fabric.html', {
																'table_list': json.dumps(table_list),
																							})

@csrf_exempt
def image_test(request):
	handle_uploaded_file(request.FILES['file'])


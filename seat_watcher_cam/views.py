from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import os

def connect_test(request):
    return HttpResponse('ok')

def send_image(request):
    if not os.path.isfile("images/captured.jpg"):
        f = open('images/origin.jpg', 'rb')
    else:
        f = open('images/captured.jpg', 'rb')
    return FileResponse(f)

def send_result(request):
    f = open('result.json', 'rb')
    return FileResponse(f)

@csrf_exempt
def get_seat_info(request):
    pos_data = request.POST['seat_data']
    f = open('pos_data.json', 'w')
    f.write(pos_data)
    f.close()
    return HttpResponse('good')
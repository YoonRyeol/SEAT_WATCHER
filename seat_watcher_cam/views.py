from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

def connect_test(request):
    return HttpResponse('ok')

def send_image(request):
    """
    Todo : 사진찍기 후 open에 경로 넣어줄 것 
    """
    f = open('Picture 38.jpg', 'rb')
    return FileResponse(f)

@csrf_exempt
def get_seat_info(request):
    pos_data = request.POST['seat_data']
    f = open('pos_data.json', 'w')
    f.write(pos_data)
    f.close()
    return HttpResponse('good')
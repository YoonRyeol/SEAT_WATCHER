from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

def connect_test(request):
    return HttpResponse('ok')

def send_image(request):
    return HttpResponse('something')

@csrf_exempt
def get_seat_info(request):
    pos_data = request.POST['seat_data']
    f = open('pos_data.json', 'w')
    f.write(pos_data)
    f.close()
    return HttpResponse('good')
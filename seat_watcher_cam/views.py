from django.shortcuts import render
from django.http import HttpResponse

def connect_test(request):
    return HttpResponse('ok')

def send_image(request):
    return HttpResponse('something')
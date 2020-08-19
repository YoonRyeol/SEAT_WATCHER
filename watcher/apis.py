from django.http import JsonResponse, HttpResponse
import requests
import json

def send_seat_data(request):
    string_data = request.POST['seat_data']
    real_data = json.loads(string_data)
    r = requests.post('http://localhost:8010/get_seat_info', data = {'seat_data':string_data}, timeout=5)
    print(real_data)
    return HttpResponse('')
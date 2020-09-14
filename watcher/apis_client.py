from django.http import JsonResponse, HttpResponse
from watcher.models import *
from .serializers import *
import requests
import json

def get_client_store_list(request) :

	stores = Store.objects.all();
	serialized_stores = StoreSerializer(stores,many=True)

	return HttpResponse(json.dumps(serialized_stores.data))

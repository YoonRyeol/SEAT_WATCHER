from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from watcher.models import *
from .serializers import *
import requests
import json

def get_client_store_list(request) :
	stores = Store.objects.all()
	paginator = Paginator(stores,5)
	pages = request.GET.get('page',1)

	try :
		stores = paginator.page(pages)
	except PageNotAnInteger :
		stores = paginator.page(0)
	except EmptyPage :
		stores = paginator.page(paginator.num_pages)
		print("last")
		return HttpResponse("end")
	
	serialized_stores = StoreSerializer(stores,many=True)

	return HttpResponse(json.dumps(serialized_stores.data))

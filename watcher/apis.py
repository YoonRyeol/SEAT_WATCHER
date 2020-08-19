from django.http import HttpResponse, JsonResponse
from watcher.models import *
import json

def get_data(request):
	pk = int(request.GET['pk'])
	camera = Camera.objects.get(pk=pk)

	output = {
		'elec_avaliable' : camera.elec_available
	} 


	return HttpResponse(json.dumps(output))

	return JsonResponse(output)
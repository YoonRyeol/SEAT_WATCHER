from django.db import models

# Create your models here.

class Camera(models.Model) :
	camera_id = models.CharField(max_length = 30)
	store_id = models.CharField(max_length = 30)
	elec_available = models.CharField(max_length = 30)
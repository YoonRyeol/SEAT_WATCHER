from rest_framework import serializers
from . import models as Models

class CameraSerializer(serializers.ModelSerializer) :
	class Meta :
		model = Models.Camera
		fields = ('pk','store_id','floor_id','cur_host','cur_pic','mac_addr','description')


class StoreSerializer(serializers.ModelSerializer) :
	class Meta :
		model = Models.Store
		fields = ('pk','store_name','store_location','picture_name','review_score')


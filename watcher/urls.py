#서브앱의 urls

from django.contrib import admin
from django.urls import path, include
from . import views
from . import apis

app_name ='watcher'

urlpatterns = [
 	path('',views.Camera_list, name='Camera_list'),
	path('table_set/', views.table_set, name='table_set'),
	path('store_info/<int:store_pk>/camera/<int:camera_pk>', views.table_set, name='table_set'),
	path('image_download', views.image_test, name='image_test'),
	path('api/send_seat_data', apis.send_seat_data, name='send_seat_data'),
	path('api/get_file_from_cam', apis.get_file_from_cam, name='get_file_from_cam'),
 ]



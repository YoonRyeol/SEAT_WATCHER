#서브앱의 urls

from django.contrib import admin
from django.urls import path, include
from . import views
from . import apis

app_name ='watcher'

urlpatterns = [
 	path('',views.Camera_list, name='Camera_list'),
	path('table_set/', views.table_set, name='table_set'),
	path('image_download', views.image_test, name='image_test'),
	path('store_list/',views.store_list, name='store_list'),
	path('store_list/<int:store_id>/',views.Camera_list, name='Camera_list'),
	path('add_store_list',apis.add_store_list, name='ajax_add_store_list'),
	path('add_camera_list',apis.add_camera_list, name='ajax_add_camera_list'),
	path('get_store_info_row',apis.get_store_info, name='ajax_get_store_info'),
	path('get_camera_info_row',apis.get_camera_info, name='ajax_get_camera_info'),	
	path('delete_camera_list',apis.delete_camera_list, name='ajax_delete_camera_list'),
	path('api/send_seat_data', apis.send_seat_data, name='send_seat_data'),
 ]



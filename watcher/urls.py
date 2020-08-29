#서브앱의 urls

from django.contrib import admin
from django.urls import path, include
from . import views
from . import apis

app_name ='watcher'

urlpatterns = [
 	path('', views.store_list, name='store_list'),
	path('table_set/', views.table_set, name='table_set'),
	path('store_info/<int:store_pk>/camera/<int:camera_pk>', views.table_set, name='table_set'),
	path('store_info/<int:store_pk>/layout/<int:floor_pk>', views.store_layout, name="store_layout"),
	path('image_download', views.image_test, name='image_test'),
	path('store_layout', views.store_layout, name='store_layout'),
	path('store_list/',views.store_list, name='store_list'),
	path('store_list/<int:store_id>/',views.Camera_list, name='Camera_list'),
	path('add_store_list',apis.add_store_list, name='ajax_add_store_list'),
	path('add_camera_list',apis.add_camera_list, name='ajax_add_camera_list'),
	path('get_store_info_row',apis.get_store_info, name='ajax_get_store_info'),
	path('get_camera_info_row',apis.get_camera_info, name='ajax_get_camera_info'),	
	path('delete_camera_list',apis.delete_camera_list, name='ajax_delete_camera_list'),
	path('cam_picture/<int:camera_pk>', views.cam_picture, name='cam_picture'),
	path('api/send_seat_data', apis.send_seat_data, name='send_seat_data'),
	path('add_floor_info',apis.add_floor_info, name='ajax_add_floor_info'),
	path('api/get_file_from_cam', apis.get_file_from_cam, name='get_file_from_cam'),
	path('api/save_layout', apis.save_layout, name='save_layout'),
	path('api/get_seat_inspection_result', apis.get_seat_inspection_result, name='get_seat_inspection_result'),
 ]



#서브앱의 urls

from django.contrib import admin
from django.urls import path, include
from . import views
from . import apis
from . import apis_client

app_name ='watcher'

urlpatterns = [
 	path('', views.store_list, name='store_info'),
	path('table_set/', views.table_set, name='table_set'),
	path('store_info/<int:store_pk>/camera/<int:camera_pk>', views.table_set, name='table_set'),
	path('store_info/<int:store_pk>/layout/<int:floor_pk>', views.store_layout, name="store_layout"),
	path('image_download', views.image_test, name='image_test'),
	path('store_layout', views.store_layout, name='store_layout'),
	path('store_list/',views.store_list, name='store_list'),
	path('store_list/<int:store_id>/',views.Camera_list, name='Camera_list'),
	path('client_page', views.client_page),
	path('client_page/<int:store_pk>', views.client_page, name='client_page'),
	path('store_info/<int:store_id>/',views.Camera_list, name='Camera_list'),
	path('store/add_store_list',apis.add_store_list, name='ajax_add_store_list'),
	path('store/delete_store_info',apis.delete_store_info,name='ajax_delete_store_info'),
	path('store/edit_store_info',apis.edit_store_info,name='ajax_edit_store_info'),
	path('store/get_store_info',apis.get_store_info, name='ajax_get_store_info'),
	path('store/get_client_store_list',apis_client.get_client_store_list, name='ajax_get_client_store_list'),
	path('camera/add_camera_info',apis.add_camera_info, name='ajax_add_camera_info'),
	path('camera/get_camera_info',apis.get_camera_info, name='ajax_get_camera_info'),
	path('camera/edit_camera_info',apis.edit_camera_info, name='ajax_edit_camera_info'),
	path('camera/delete_camera_list',apis.delete_camera_list, name='ajax_delete_camera_list'),
	path('camera/get_camera_info_without_floor',apis.get_camera_info_without_floor, name='get_camera_info_without_floor'),
	path('camera/check_camera_connection',apis.check_camera_connection, name='ajax_check_camera_connection'),
	path('camera/check_camera_connection_table',apis.check_camera_connection_table, name='ajax_check_camera_connection_table'),
	path('floor/add_floor_info',apis.add_floor_info, name='ajax_add_floor_info'),
	path('floor/edit_floor_id',apis.edit_floor_id, name='ajax_edit_floor_id'),
	path('floor/delete_floor_info',apis.delete_floor_info, name='ajax_delete_floor_info'),
	path('floor/edit_floor_camera_list',apis.edit_floor_camera_list,name='ajax_edit_floor_camera_list'),
	path('api/get_file_from_cam', apis.get_file_from_cam, name='get_file_from_cam'),
	path('api/save_layout', apis.save_layout, name='save_layout'),
	path('api/get_seat_inspection_result', apis.get_seat_inspection_result, name='get_seat_inspection_result'),
	path('api/send_seat_data', apis.send_seat_data, name='send_seat_data'),
	path('cam_picture/<int:camera_pk>', views.cam_picture, name='cam_picture'),
	path('api/save_layout', apis.save_layout, name='save_layout'),
	path('client',views.client_store_list,name='client_store_list'),
 ]




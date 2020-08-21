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
	path('store_list_row',apis.get_store_list, name='ajax_get_store_list'),
	path('add_store_list',apis.add_store_list, name='ajax_add_store_list'),
	path('camera_list_row',apis.get_camera_list, name='ajax_get_camera_list'),
	path('store_list/<int:store_id>/',views.Camera_list, name='Camera_list'),
	path('send_store_pk',apis.send_store_pk, name='ajax_send_store_pk'),
 ]



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
	path('store_layout', views.store_layout, name='store_layout'),
	path('api/send_seat_data', apis.send_seat_data, name='send_seat_data'),
 ]



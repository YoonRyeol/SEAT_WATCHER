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
 ]



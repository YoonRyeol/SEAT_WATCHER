#서브앱의 urls

from django.contrib import admin
from django.urls import path, include
from . import views

app_name ='watcher'

urlpatterns = [
 	path('',views.Get_Camera_list, name='Camera_list'),
 ]




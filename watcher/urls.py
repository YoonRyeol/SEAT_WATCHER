#서브앱의 urls

from django.contrib import admin
from django.urls import path, include
from . import views
from . import apis
from . import apis_client
from django.conf.urls.static import static
from django.conf import settings

app_name ='watcher'

urlpatterns = [
 	path('',views.Get_Camera_list, name='Camera_list'),
 	path('guest_page/',views.Guest_page, name ='Guest_page'),
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
	path('store/upload_store_name',apis.upload_store_img, name='ajax_upload_store_img'),
	path('camera/add_camera_info',apis.add_camera_info, name='ajax_add_camera_info'),
	path('camera/get_camera_info',apis.get_camera_info, name='ajax_get_camera_info'),
	path('camera/edit_camera_info',apis.edit_camera_info, name='ajax_edit_camera_info'),
	path('camera/delete_camera_list',apis.delete_camera_list, name='ajax_delete_camera_list'),
	path('camera/get_camera_info_without_floor',apis.get_camera_info_without_floor, name='get_camera_info_without_floor'),
	path('camera/check_camera_connection',apis.check_camera_connection, name='ajax_check_camera_connection'),
	path('camera/check_camera_connection_row',apis.check_camera_connection_row, name='ajax_check_camera_connection_row'),
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
	path('api/localize_object', apis.localize_objects, name='localize_object'),
	path('client/search',apis_client.search_client_store_list, name='ajax_search_client_store_list'),
	path('client/liked',apis_client.client_liked_list,name='ajax_client_liked_list'),
	path('api/update_cam_addr', apis.update_cam_addr, name='update_cam_addr'),
	path('client/signup',views.client_signup,name='client_signup'),
	path('api/client_signup', apis_client.client_signup, name='ajax_client_signup'),
	path('api/client_logout', apis_client.client_logout, name='ajax_client_logout'),
	path('client/signin', views.client_signin, name='client_signin'),
	path('api/client_signin', apis_client.client_signin, name='ajax_client_signin'),
	path('api/save_review', apis_client.save_review, name='ajax_save_review'),
	path('client/map/', views.client_map, name='client_map'),
	path('store_info/<int:store_pk>/menu', views.store_menu, name='store_menu'),
	path('store_info/<int:store_pk>/menu/add', views.store_menu_add, name='store_menu_add'),
	path('api/add_category_info', apis.add_category_info, name='ajax_add_category_info'),
	path('api/add_store_menu_info', apis.add_store_menu_info, name='ajax_add_store_menu_info'),
	path('api/edit_store_menu_info', apis.edit_store_menu_info, name='ajax_edit_store_menu_info'),
	path('api/delete_store_menu_info', apis.delete_store_menu_info, name='ajax_delete_store_menu_info'),

	

 ]




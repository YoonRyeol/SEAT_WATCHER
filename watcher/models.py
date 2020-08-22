from django.db import models

# Create your models here.

class Store(models.Model):
    store_name = models.CharField(max_length=256, blank=True, null=True)
    store_location = models.CharField(max_length=256, blank=True, null=True)

class Camera(models.Model):
    store = models.ForeignKey('Store', on_delete=models.SET_NULL, blank=True, null=True)
    cur_pic = models.CharField(max_length=256, blank=True, null=True)
    mac_addr = models.CharField(max_length=256, blank=True, null=True)
    cur_host = models.CharField(max_length=256, blank=True, null=True)
    description = models.CharField(max_length=1024, blank=True, null=True)

class Table(models.Model):
    store = models.ForeignKey('Store', on_delete=models.SET_NULL, blank=True, null=True)
    camera = models.ForeignKey('Camera', on_delete=models.SET_NULL, blank=True, null=True)
    pic_name = models.CharField(max_length=256, blank=True, null=True)
    pic_f_x = models.FloatField(blank=True, null=True)
    pic_f_y = models.FloatField(blank=True, null=True)
    pic_s_x = models.FloatField(blank=True, null=True)
    pic_s_y = models.FloatField(blank=True, null=True)
    layout_f_x = models.FloatField(blank=True, null=True)    
    layout_f_y = models.FloatField(blank=True, null=True)    
    layout_s_x = models.FloatField(blank=True, null=True)    
    layout_s_y = models.FloatField(blank=True, null=True)    
    is_elec = models.BooleanField(default=False)
    capacity = models.IntegerField(default=-1) 
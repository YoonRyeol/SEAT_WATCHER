from django.db import models

# Create your models here.
class Store(models.Model):
    store_name = models.CharField(max_length=256, blank=True, null=True)
    store_location = models.CharField(max_length=256, blank=True, null=True)
    picture_name = models.CharField(max_length=256, blank=True, null=True)
    review_score = models.DecimalField(max_digits=3, decimal_places=2)

class Camera(models.Model):
    store = models.ForeignKey('Store', on_delete=models.SET_NULL, blank=True, null=True)
    floor = models.ForeignKey('Floor', on_delete=models.SET_NULL, blank=True, null=True)
    cur_pic = models.CharField(max_length=256, blank=True, null=True)
    mac_addr = models.CharField(max_length=256, blank=True, null=True)
    cur_host = models.CharField(max_length=256, blank=True, null=True)
    description = models.CharField(max_length=1024, blank=True, null=True)

class Table(models.Model):
    store = models.ForeignKey('Store', on_delete=models.SET_NULL, blank=True, null=True)
    floor = models.ForeignKey('Floor', on_delete=models.SET_NULL, blank=True, null=True)
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
    is_occupied = models.BooleanField(default=False)

class Floor(models.Model):
    store = models.ForeignKey('Store', on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=256, blank=True, null=True)
    floor_num = models.IntegerField(default=-1)
    description = models.CharField(max_length=1024, blank=True, null=True)

class User(models.Model) :
    user_id = models.CharField(primary_key=True,max_length=128)
    password = models.CharField(max_length=128, blank=True, null=True)

class Review(models.Model) :
    store = models.ForeignKey('Store', on_delete=models.SET_NULL,blank=True,null=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE,blank=True)
    score = models.FloatField(blank=True, default=0)
    date = models.CharField(max_length=128, blank=True, null=True)
    comment = models.TextField(max_length=500, blank=True, null= True)

class Category(models.Model):
    store = models.ForeignKey('Store', on_delete=models.SET_NULL,blank=True,null=True)
    name = models.CharField(max_length=128, blank=True, null= True)


class Menu(models.Model):
    store = models.ForeignKey('Store', on_delete=models.SET_NULL,blank=True,null=True)
    name = models.CharField(max_length=128, blank=True, null= True)
    price = models.CharField(max_length=128, blank=True, null= True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL,blank=True,null=True)
    category_name =models.CharField(max_length=128, blank=True, null= True)

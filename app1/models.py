from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class UserInfo(models.Model) :
    user  =  models.OneToOneField(User , on_delete=models.CASCADE)
    phone_number =  models.CharField(max_length=15)
    address  =  models.CharField(max_length=500)
    pancard_number  =  models.CharField(max_length=30)
    user_image =  models.ImageField()
    pancard_image =  models.ImageField()

# ImageFiled in Models
#  pip  install pillow
#  media url in setting
#  static url  in urls.py

class Stocks(models.Model):
    ticker   =  models.CharField(max_length=10)
    name =  models.CharField(max_length=300)
    description  =  models.CharField(max_length =5000)
    curr_price =  models.FloatField()

    def __str__(self):
        return  self.name


# Fk is many to one

class  UserStock(models.Model) :
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stocks, on_delete=models.CASCADE)
    purchase_price =  models.FloatField()
    purchase_quantity  = models.IntegerField()
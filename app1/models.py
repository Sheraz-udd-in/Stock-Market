from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserInfo(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=500)
    pancard_number = models.CharField(max_length=30)
    user_image = models.ImageField()
    pancard_image = models.ImageField()
    def __str__(self):
        return self.user.username

# models.py
class Stocks(models.Model):
    ticker = models.CharField(max_length=10)
    name = models.CharField(max_length=300)
    description = models.CharField(max_length=5000)
    curr_price = models.FloatField()
    quantity = models.PositiveIntegerField(default=0)  # Add this line

    def __str__(self):
        return f"{self.ticker} - {self.name}"



class UserStock(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stocks,on_delete=models.CASCADE)
    purchased_price = models.FloatField()
    purchased_quantity = models.IntegerField()
    def __str__(self):
        return f"{self.user.username} owns {self.stock.ticker}"

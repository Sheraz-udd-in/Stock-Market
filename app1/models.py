from django.db import models

# Create your models here.
class Stocks(models.Model):
    ticker = models.CharField(max_length=10)
    name = models.CharField(max_length= 300)
    Description = models.CharField(max_length=5000)
    Current_price = models.FloatField()
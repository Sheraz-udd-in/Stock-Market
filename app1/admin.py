from django.contrib import admin

from app1.models import Stocks,UserInfo

# Register your models here.
admin.site.register(Stocks)
admin.site.register(UserInfo)
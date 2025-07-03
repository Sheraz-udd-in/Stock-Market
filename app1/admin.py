from django.contrib import admin

from app1.models import Stocks,UserInfo,UserStock

# Register your models here.
admin.site.register(Stocks)
admin.site.register(UserInfo)
admin.site.register(UserStock)

class StockAdmin(admin.ModelAdmin):
    list_display = ('ticker', 'name', 'curr_price')
    search_fields = ('ticker', 'name')
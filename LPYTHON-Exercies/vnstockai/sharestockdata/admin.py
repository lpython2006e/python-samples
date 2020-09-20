from django.contrib import admin
from .models import StockInfo, StockDayData, StockPriceData, StockTransactions
# Register your models here.

admin.site.register(StockInfo)
admin.site.register(StockDayData)
admin.site.register(StockPriceData)
admin.site.register(StockTransactions)

from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(StockInfo)
admin.site.register(StockDayData)
admin.site.register(StockPriceData)
admin.site.register(StockTransactions)
admin.site.register(StockOrder)
admin.site.register(testData)

from django.db import models


# Create your models here.

# thong tin website
class StockInfo(models.Model):
    exchange = models.TextField(max_length=10)
    code = models.TextField(max_length=3)
    name = models.TextField()
    cafef_link = models.TextField()
    vietstock_link = models.TextField()
    website = models.TextField()


# THông tin chứng khoán trong ngày
class StockDayData(models.Model):
    day = models.DateField()
    code = models.TextField(max_length=3)
    min_price = models.IntegerField()
    ref_price = models.IntegerField()
    max_price = models.IntegerField()
    min_bought_price = models.IntegerField()
    max_bought_price = models.IntegerField()


# Các giao dịch xảy ra trong ngày
class StockTransactions(models.Model):
    time = models.DateTimeField()
    code = models.TextField(max_length=3)
    volume = models.IntegerField()
    price = models.IntegerField()


# Giá thay đổi trong ngày
class StockPriceData(models.Model):
    code = models.TextField(max_length=3)
    time = models.DateTimeField()
    price = models.IntegerField()

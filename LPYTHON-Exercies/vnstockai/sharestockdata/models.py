from django.db import models


# Create your models here.

# thong tin website
class StockInfo(models.Model):
    #san
    exchange = models.TextField(max_length=10)
    #ma chung khoang vd AAA
    code = models.TextField(max_length=3)
    # ten cua cong ty
    name = models.TextField()
    #link cong ty
    cafef_link = models.TextField()
    # website cong ty
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

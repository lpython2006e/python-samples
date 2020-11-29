from django.db import models


# Create your models here.

# thong tin website
class StockInfo(models.Model):
    # san
    exchange = models.TextField(max_length=10)
    # ma chung khoang vd AAA
    code = models.TextField(max_length=3)
    # ten cua cong ty
    name = models.TextField()
    # link cong ty
    cafef_link = models.TextField()
    # website cong ty
    website = models.TextField()


# THông tin chứng khoán trong ngày
class StockDayData(models.Model):
    day = models.DateField()
    code = models.TextField(max_length=3)
    min_price = models.FloatField()  # gia san
    ref_price = models.FloatField()  # gia tham chieu (gia ngay hom trc)
    max_price = models.FloatField()  # gia tran
    min_bought_price = models.FloatField()  # gia cao nhat cua than cay nen
    max_bought_price = models.FloatField()  # gia thap nhat cua than cay nen
    open_price = models.FloatField(default=0)  # gia mo cua


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


class StockOrder(models.Model):
    time = models.DateTimeField()
    code = models.TextField(max_length=3)
    volume = models.IntegerField()
    price = models.IntegerField()
    # type mua ban


class testData(models.Model):
    day = models.DateField()
    min_order = models.IntegerField()
    max_order = models.IntegerField()
    volume = models.IntegerField()
    change_limit = models.FloatField()

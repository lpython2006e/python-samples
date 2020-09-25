# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_djangoitem import DjangoItem
from sharestockdata.models import StockPriceData, StockTransactions, StockDayData, StockInfo


class StockPriceDataItem(DjangoItem):
    django_model = StockPriceData


class StockTransactionsItem(DjangoItem):
    django_model = StockTransactions


class StockDayDataItem(DjangoItem):
    django_model = StockDayData


class StockInfoItem(DjangoItem):
    django_model = StockInfo


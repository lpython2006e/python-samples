from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst
import re
import csv
import scrapy
import json
from livestockclawling.livestockclawling.items import StockDayDataItem, StockInfoItem, StockPriceDataItem, \
    StockTransactionsItem
import datetime

dataName = []
dayName = []
with open('datacsv.csv', 'r') as csv_file:
    csv_header = csv.reader(csv_file)

    for line in csv_header:
        dataName.append(line[0])
        dayName.append(line[1])
    dataName.pop(0)
    dayName.pop(0)


class PropertiesSpider(scrapy.Spider):
    mapped_data = {}
    name = 'cafeftest'
    start_urls = ['https://banggia.cafef.vn/stockhandler.ashx?center=2']
    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "vi-VN, vi;q=0.9, en-US;q=0.8, en;q=0.7",
        # "Referer": "https://banggia.cafef.vn/stockhandler.ashx",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0(Windows NT 10.0; WOW64) AppleWebKit/537.36(KHTML, likeGecko) coc_coc_browser/89.0.124 Chrome/83.0.4103.124 Safari/537.36"
    }

    def parse(self, response):
        raw_data = response.body
        data = json.loads(raw_data)
        urlCompanyDetailExtract = 'https://s.cafef.vn/Lich-su-giao-dich-{0}-6.chn?date=27/10/2020'  # change time
        limit = 5
        count = 0
        for stock in data:
            try:
                if count > limit:
                    break
                i = StockTransactionsItem()
                i['code'] = dataName[count]
                self.compose_data_final(i)

                # name_company
                extract_company_detail_url = urlCompanyDetailExtract.format(i['code'].upper())
                print('Making request: ' + extract_company_detail_url)
                count += 1
                yield scrapy.Request(
                    extract_company_detail_url,
                    callback=self.parse_cafef_details_company,
                    headers=self.headers
                )

            except Exception as err:
                print('Data error: ' + err)

    def parse_cafef_details_company(self, response):
        val_try = int(float(response.xpath('count(//*[@id="tblData"]/tr)').get()))
        if val_try >= 1:
            for i in range(1, val_try + 1):
                code = response.url[37:40]

                temp_time = response.xpath(('//*[@id="tblData"]/tr[{}]/td[1]/text()').format(i)).get()
                time = datetime.datetime.strptime(temp_time, '%H:%M:%S')
                price = float(response.xpath(('//*[@id="tblData"]/tr[{}]/td[2]/text()').format(i)).get())
                volume_temp = (response.xpath(('//*[@id="tblData"]/tr[{}]/td[3]/text()').format(i)).get())
                if volume_temp.find(',') != -1:
                    volume = int(volume_temp.replace(',', ''))
                else:
                    volume = int(volume_temp)
                data_final = self.compose_data_final(None, code, time, volume, price)

                yield data_final

    def compose_data_final(self, stock_info_item: StockTransactionsItem = None, code: str = None, time: datetime = None,
                           volume: float = None,
                           price: float = None):
        if stock_info_item:
            self.mapped_data[stock_info_item['code']] = stock_info_item
        if code is None:
            return self.mapped_data[stock_info_item['code']]
        if time:
            self.mapped_data[code.strip()]['time'] = time
        if volume:
            self.mapped_data[code.strip()]['volume'] = volume

        if price:
            self.mapped_data[code.strip()]['price'] = price
        return self.mapped_data[code.strip()]

class Stock_day:
    def __init__(self,code,time,volume,price):
        self.time=None
        self.code=None
        self.volume=None
        self.price=None

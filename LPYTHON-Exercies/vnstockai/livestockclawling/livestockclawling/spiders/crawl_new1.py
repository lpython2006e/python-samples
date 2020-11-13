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
        urlCompanyDetailExtract = 'https://s.cafef.vn/Lich-su-giao-dich-{0}-6.chn?date=29/10/2020' # change time
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
        for i in range(1, 2):# cho nay sua lai tu 1 den 250 hoac nho hon 250
            code = response.url[37:40]
            # time = float(response.xpath(('//*[@id="tblData"]/tbody/tr[{}]/td[1]/text()').format(i)).get())
            # price = float(response.xpath(('//*[@id="tblData"]/tbody/tr[{}]/td[2]/text()/text()').format(i)).get())
            time = '2012-09-04 06:00'
            price = 2.7
            volume = 100
            data_final = self.compose_data_final(None, code, time, price)
            # time price volume trong bang lay khong duoc, xpath ra None, thu dung selector,time price volume o tren de thu lay dc du lieu chua

            yield data_final

    def compose_data_final(self, stock_info_item: StockTransactionsItem = None, code: str = None, time: float = None,
                           price: float = None):
        if stock_info_item:
            self.mapped_data[stock_info_item['code']] = stock_info_item
        if code is None:
            return self.mapped_data[stock_info_item['code']]
        if time:
            self.mapped_data[code.strip()]['time'] = time
        # if volume:
        #     self.mapped_data[code.strip()]['time'] = volume
        # neu lay dc volume thi bo comment doan nay
        if price:
            self.mapped_data[code.strip()]['price'] = price
        return self.mapped_data[code.strip()]


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
open_price=[]
# file csv nay down tren trang download
with open('datacsv.csv', 'r') as csv_file:
    csv_header = csv.reader(csv_file)

    for line in csv_header:
        dataName.append(line[0])
        dayName.append(line[1])
        open_price.append(line[2])
    dataName.pop(0)
    dayName.pop(0)
    open_price.pop(0)

class PropertiesSpider(scrapy.Spider):
    mapped_data = {}
    name = 'cafeftest'
    start_urls = ['https://banggia.cafef.vn/stockhandler.ashx?center=2']
    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "vi-VN, vi;q=0.9, en-US;q=0.8, en;q=0.7",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0(Windows NT 10.0; WOW64) AppleWebKit/537.36(KHTML, likeGecko) coc_coc_browser/89.0.124 Chrome/83.0.4103.124 Safari/537.36"
    }

    def parse(self, response):
        raw_data = response.body
        data = json.loads(raw_data)
        urlCompanyDetailExtract = 'https://s.cafef.vn/Lich-su-giao-dich-{0}-6.chn?date=29/10/2020'


        limit = 5
        count = 0
        for stock in data:
            try:
                if count > limit:
                    break
                i = StockDayDataItem()
                i['day'] = int(dayName[count])
                i['code'] = dataName[count]
                i['open_price']=open_price[count]
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
    #den tung trang extract data
    #tran san dung max min +-10%
    def parse_cafef_details_company(self, response):
        temp_name = response.xpath('//*[@id="ctl00_Head1"]/title/text()').get()
        search = re.search("([\w\s]*):([\w\s]*)", temp_name.strip(), re.DOTALL)
        code = search.group(1)
        cafe_link = response.url
        minPrice = float(response.xpath('//*[@id="price-box"]/span[6]/text()').get())
        maxPrice = float(response.xpath('//*[@id="price-box"]/span[4]/text()').get())
        refPrice = float(response.xpath('//*[@id="price-box"]/span[2]/text()').get())
        tran = round(maxPrice*1.1,2)
        san = round(minPrice*0.9,2)




        data_final = self.compose_data_final(None, code, minPrice, maxPrice, refPrice,tran,san)

        yield data_final

    def compose_data_final(self, stock_info_item: StockDayDataItem = None, code: str = None, minPrice: float = None,
                           maxPrice: float = None, refPrice: float = None,tran: float=None,san: float=None,open:float=None):
        if stock_info_item:
            self.mapped_data[stock_info_item['code']] = stock_info_item
        if code is None:
            return self.mapped_data[stock_info_item['code']]
        if minPrice:
            self.mapped_data[code.strip()]['min_price'] = minPrice
        if maxPrice:
            self.mapped_data[code.strip()]['max_price'] = maxPrice
        if refPrice:
            self.mapped_data[code.strip()]['ref_price'] = refPrice
        if tran:
            self.mapped_data[code.strip()]['max_bought_price'] = tran
        if san:
            self.mapped_data[code.strip()]['min_bought_price'] = san
        if open:
            self.mapped_data[code.strip()]['open_price'] = open
        return self.mapped_data[code.strip()]

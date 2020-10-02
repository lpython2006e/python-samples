import scrapy
import json
from livestockclawling.livestockclawling.items import StockDayDataItem, StockInfoItem, StockPriceDataItem, \
    StockTransactionsItem


class cafeftest(scrapy.Spider):
    name = 'cafeftest'
    start_urls = ['https://banggia.cafef.vn/stockhandler.ashx?center=undefined']
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
        for stock in data:
            try:
                # yield scrapy.Request(
                #     url,
                #     callback=self.parse_item,
                #     headers=self.headers,
                #     body=stock.__str__()
                # )
                # yield stock
                i = StockInfoItem()
                i['exchange'] = 'HOSE'
                i['code'] = stock['a']
                i['name'] = 'default'
                i['cafef_link'] = 'default'
                i['website'] = 'default'
                yield i
            except Exception as err:
                print('Data error: ' + err)

    def parse_dynamic_url(self, response):
        url = 'https://banggia.cafef.vn/.../???.chn'
        # Get from database all the codes

        for code in codes:
            try:
                yield scrapy.Request(
                    url + code + ".chn",
                    callback=self.parse_cafef_details_company,
                    headers=self.headers
                )
            except Exception as err:
                print('Data error: ' + err)

    def parse_cafef_details_company(self, response):
        i = StockInfoItem()
        i['exchange'] = 'HOSE'
        i['code'] = response['a']
        i['name'] = 'default'
        i['cafef_link'] = 'default'
        i['website'] = 'default'
        yield i

    def parse_item(self, response):
        i = StockInfoItem()
        i['exchange'] = 'HOSE'
        i['code'] = response['a']
        i['name'] = 'default'
        i['cafef_link'] = 'default'
        i['website'] = 'default'
        return i

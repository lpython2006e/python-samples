import scrapy
import json


class shsstock(scrapy.Spider):
    name = 'cafeftock'
    start_urls = ['https://liveboard.cafef.vn/']
    headers = {
        "Accept": "application/json, text/javascript, */*; q = 0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "vi-VN, vi;q=0.9, en-US;q=0.8, en;q=0.7",
        "Referer": "https://liveboard.cafef.vn/",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0(Windows NT 10.0; WOW64) AppleWebKit/537.36(KHTML, likeGecko) coc_coc_browser/89.0.124 Chrome/83.0.4103.124 Safari/537.36"
    }

    def parse(self, response):
        url = ['https://banggia.cafef.vn/stockhandler.ashx?center=undefined']
        raw_data = response.body
        data = json.loads(raw_data)
        for stock in data:
            yield scrapy.Request(
                url,
                headers=self.headers
            )

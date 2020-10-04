import re

import scrapy
import json
from livestockclawling.livestockclawling.items import StockDayDataItem, StockInfoItem, StockPriceDataItem, \
    StockTransactionsItem


class cafeftest(scrapy.Spider):

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
        urlCompanyDetailExtract = 'https://s.cafef.vn/hastc/{0}-whatever.chn'
        urlWebsiteExtract = 'https://s.cafef.vn/Ajax/CongTy/ThongTinChung.aspx?sym={0}'

        limit = 2
        count = 0
        for stock in data:
            try:
                count += 1
                if count > limit:
                    break
                i = StockInfoItem()
                i['exchange'] = 'HSX'
                i['code'] = stock['a']
                self.compose_data_final(i)

                # website
                website_extract_format = urlWebsiteExtract.format(i['code'].lower())
                print('Making request: ' + website_extract_format)
                yield scrapy.Request(
                    website_extract_format,
                    callback=self.parse_cafef_website,
                    headers=self.headers
                )

                # name_company
                extract_company_detail_url = urlCompanyDetailExtract.format(i['code'].lower())
                print('Making request: ' + extract_company_detail_url)
                yield scrapy.Request(
                    extract_company_detail_url,
                    callback=self.parse_cafef_details_company,
                    headers=self.headers
                )

            except Exception as err:
                print('Data error: ' + err)


    def parse_cafef_website(self, response):
        websiteURL = response.xpath('//*[text() = \'Website:\']/following-sibling::a[1]').attrib['href']
        print('Extracted Website URL: ' + websiteURL)
        code = response.url[-3:].upper()
        data_final = self.compose_data_final(None, code, None, None, websiteURL)
        if data_final['name'] and data_final['website']:
            yield data_final

    def parse_cafef_details_company(self, response):
        temp_name = response.xpath('//*[@id="ctl00_Head1"]/title/text()').get()
        search = re.search("([\w\s]*):([\w\s]*)", temp_name.strip(), re.DOTALL)
        code = search.group(1)
        name = search.group(2)
        cafe_link = response.url
        print('Extracted Details: ' + name)
        data_final = self.compose_data_final(None, code, name, cafe_link, None)
        if data_final['name'] and data_final['website']:
            yield data_final

    def compose_data_final(self, stock_info_item: StockInfoItem=None, code: str=None, company_name: str=None, cafef_link: str=None, website: str=None):
        if stock_info_item:
            self.mapped_data[stock_info_item['code']] = stock_info_item
        if code is None:
            return self.mapped_data[stock_info_item['code']]
        if company_name:
            self.mapped_data[code.strip()]['name'] = company_name
        if cafef_link:
            self.mapped_data[code.strip()]['cafef_link'] = cafef_link
        if website:
            self.mapped_data[code.strip()]['website'] = website
        return self.mapped_data[code.strip()]
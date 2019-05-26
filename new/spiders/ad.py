# -*- coding: utf-8 -*-
import scrapy
from new.items import NewItem
from scrapy import cmdline
import json
from copy import copy


class AdSpider(scrapy.Spider):


    name = 'ad'
    # allowed_domains = ['baidu.com']
    start_urls = ['http://baidu.com/','https://fe-api.zhaopin.com/c/i/sou?pageSize=90&cityId=635&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kw=Python&kt=3&rt=58e76b0c8b854ec79faac276f2f2a4b3&_v=0.06339982&x-zp-page-request-id=f88b73fd1755424aa2caf4b7ab893363-1557825416958-371535']
    use =   {"USER_AGENT" :"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"}
    url = 'https://fe-api.zhaopin.com/c/i/sou?start={}&pageSize=90&cityId=635&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kw=Python&kt=3&rt=58e76b0c8b854ec79faac276f2f2a4b3&_v=0.06339982&x-zp-page-request-id=f88b73fd1755424aa2caf4b7ab893363-1557825416958-371535'
    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls[1],
            headers=self.use
        )

    def parse(self, response):
        # self.crawler.stats.set_value("key","value")
        # return NewItem()
        data = json.loads(response.text)

        results = data["data"]["results"]
        for i in results:
            c = {}
            c["salary"] = i["salary"]

        start = 90
        yield scrapy.Request(
            url=self.url.format(str(start)),
            headers=self.use,
            callback=self.haha,
            meta={"start":start}

        )

    def haha(self,response):
        start = response.meta["start"]
        start = int(start) + 90
        data = json.loads(response.text)

        results = data["data"]["results"]
        for i in results:
            c = {}
            c["salary"] = i["salary"]
            yield c
        yield scrapy.Request(
            url=self.url.format(str(start)),
            headers=self.use,
            callback=self.haha,
            meta=copy({"start":str(start)})
        )





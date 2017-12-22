# -*- coding: utf-8 -*-
import scrapy
from meizitu.items import MeizituItem


class MeiziSpider(scrapy.Spider):
    name = 'meizi'
    allowed_domains = ['meizitu.com']
    _url = 'http://meizitu.com/a/more_'
    offset = 1
    start_urls = [_url + str(offset) + ".html"]

    def parse(self, response):
        url_list = response.xpath('//h3[@class="tit"]/a/@href').extract()
        for url in url_list:
            yield scrapy.Request(url=url, callback=self.parse_item)

        if self.offset < 72:
            self.offset += 1
        yield scrapy.Request(self._url + str(self.offset) + ".html", callback=self.parse)

    def parse_item(self, response):
        item_url_list = response.xpath('//div[@id="picture"]//img/@src').extract()
        # item_url_list = response.xpath('//img[@class ="scrollLoading"]/@src').extract()
        for url in item_url_list:
            item = MeizituItem()
            item['url'] = url

            yield item

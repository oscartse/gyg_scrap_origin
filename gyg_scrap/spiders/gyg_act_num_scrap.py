# -*- coding: utf-8 -*-
import scrapy
from ..items import GygScrapItem
from datetime import datetime
import requests
from lxml import etree

LUMINATI_PASS = "hja29x3mhtyy"
LUMINATI_USER = "lum-customer-klook-zone-shared_data_center"
LUMINATI_HOST = "zproxy.lum-superproxy.io"
LUMINATI_PORT = 22225


def get_proxy_credentials():
    proxy = "{}:{}@{}:{}".format(LUMINATI_USER, LUMINATI_PASS, LUMINATI_HOST, LUMINATI_PORT)
    # lum-customer-klook-zone-shared_data_center:hja29x3mhtyy@zproxy.lum-superproxy.io:22225
    return proxy

# def check_whether_city_or_attraction(request_url):
#     req = requests.request("POST", request_url)
#     root = etree.HTML(req.content)
#     checker = root.xpath('//div[@class="vertical-activity-card-container "]//text()')
#     return True if checker != 0 else False


class GygActNumScrapSpider(scrapy.Spider):
    name = 'gyg_act_num_scrap'
    allowed_domains = ['getyourguide.com']
    start_urls = ['https://www.getyourguide.com/destinations/']

    def parse(self, response):
        for link in response.xpath('//div[@class="destinations col-sm-4 col-lg-2"]/ul/li/a'):
            country_name = link.xpath('text()').extract()[0]
            req_url = link.xpath('@href').extract()[0]
            yield scrapy.Request(req_url, callback=self.parse_country, meta={'country_name': country_name})

    def parse_country(self, response):
        item = GygScrapItem()
        for country in response.xpath('//ul[@class="destinations-list destination-list--columns nav"]/li'):
            proxies = {"http": get_proxy_credentials(), }
            req = requests.request("POST", country.xpath('a/@href').extract()[0], proxies=proxies)
            root = etree.HTML(req.content)
            checker = root.xpath('//div[@class="vertical-activity-card-container "]//text()')
            if checker:
                item["city"] = country.xpath("a/text()").extract()[0]
                try:
                    country.xpath("span/text()").extract()
                    item["count"] = int("".join([i for i in country.xpath("span/text()").extract()[0] if i.isdigit()]))
                except IndexError:
                    item["count"] = "no_count"
                now = datetime.now()
                item["scrap_date"] = now.strftime("%Y-%m-%d")
                item["scrap_time"] = now.strftime("%H:%M")
                item["request_url"] = country.xpath('a/@href').extract()[0]
                item["country"] = response.meta['country_name']
                yield item

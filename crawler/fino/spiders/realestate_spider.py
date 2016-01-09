# -*- coding: utf-8 -*-

import scrapy
import pdb
import time
import datetime

from scrapy.loader.processors import MapCompose

from fino.spiders.spiderhelper import SpiderHelper
from fino.items import RealEstateItem 
from fino.itemloaders import RealEstateItemLoader


class RealEstateSpider(scrapy.Spider):
    name = "realEstate"
    start_urls = ["http://m.finn.no/realestate/homes/search.html?location=0.20003&location=1.20003.20045"]


    def parse(self, response):
        for url in response.xpath("//div[@class='flex-unit']/a/@href").extract():
            follow_url = "http://m.finn.no" + url
            yield scrapy.Request(follow_url, self.parse_realEstate_page)

    def parse_realEstate_page(self, response):
        item = RealEstateItem()

        item["url"] = response.url
        item["finnCode"] = SpiderHelper.getCodeFromRawUrl(response.url)
        item["isNewBuilding"] = "newbuildings" in response.url
        item["crawlTime"] = datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S") 

        l = RealEstateItemLoader(item = item, response = response)

        l.add_xpath("title", '//h1/text()')
        l.add_xpath("address", '//h1/following-sibling::p[1]/text()')
        
        l.add_xpath("askingPrice", '//div[@data-automation-id = "key" and text() = "Pris"]/following-sibling::div[@data-automation-id = "value"]/text()', MapCompose(SpiderHelper.normalizeNumber))
        l.add_xpath("askingPrice", '//h1/following-sibling::dl[1]/dd/text()', MapCompose(SpiderHelper.normalizeNumber))

        numberFields = {  "Verditakst"    : "verditakst",\
                          "netakst"       : "laanetakst",\
                          "Fellesformue"  : "fellesformue",\
                          "Felleskost"    : "felleskost",\
                          u"Prim"         : "primaerrom",\
                          "Bruksareal"    : "bruksareal",\
                          "Bruttoareal"   : "bruttoareal",\
                          "Tomteareal"    : "tomteareal",\
                          "Rom"           : "rom", \
                          "Bygge"         : "byggeaar", \
                          "Etasje"        : "etasje", \
                          "Soverom"       : "soverom"}

        oneWordTextFields = {    "Boligtype"     : "boligtype", \
                          "Energimerking" : "energimerking", \
                          "Eieform"       : "eieform" }

        xpathTemplate = "//h1/following-sibling::dl/dt[@data-automation-id='key' and contains(text(), '{0}')]/following-sibling::dd[1]/text()"
        
        for k, v in numberFields.items():
            xpath = xpathTemplate.format(k)
            l.add_xpath(v, xpath, MapCompose(SpiderHelper.normalizeNumber)) 
        for k, v in oneWordTextFields.items():
            xpath = xpathTemplate.format(k)
            l.add_xpath(v, xpath, MapCompose(SpiderHelper.normalizeOneWordValue))

        yield l.load_item()






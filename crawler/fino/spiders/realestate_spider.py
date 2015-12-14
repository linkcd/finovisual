# -*- coding: utf-8 -*-

import scrapy
import pdb
import re
from fino.items import RealEstateItem 
from fino.itemloaders import RealEstateItemLoader
from scrapy.loader.processors import MapCompose
import time
import datetime

class RealEstateSpider(scrapy.Spider):
    name = "realEstate"
    start_urls = ["http://m.finn.no/realestate/homes/search.html?location=0.20003&location=1.20003.20045"]

    @staticmethod
    def getCodeFromRawUrl(rawUrl):
        #get finncode
        from urlparse import urlsplit
        url_data = urlsplit(rawUrl)
        from urlparse import parse_qs
        qs_data = parse_qs(url_data.query)
        return qs_data["finnkode"][0]

    @staticmethod
    def normalizeNumber(number):
        result = "".join(re.findall('\d+', number.replace(" ", "")))
        if result.isdigit():
            return result
        else:
            return None

    @staticmethod
    def normalizeOneWordValue(rawOneWordValue):
        toremove = dict.fromkeys((ord(c) for c in u'\n '))
        return rawOneWordValue.translate(toremove)

    def parse(self, response):
        for url in response.xpath("//div[@class='flex-unit']/a/@href").extract():
            follow_url = "http://m.finn.no" + url
            yield scrapy.Request(follow_url, self.parse_realEstate_page)

    def parse_realEstate_page(self, response):
        #from scrapy.shell import inspect_response
        #inspect_response(response, self)
        item = RealEstateItem()

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
        
        item["url"] = response.url
        item["finnCode"] = self.getCodeFromRawUrl(response.url)
        item["isNewBuilding"] = "newbuildings" in response.url
        item["crawlTime"] = datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S") 
        l = RealEstateItemLoader(item = item, response = response)
        l.add_xpath("title", '//h1/text()')
        l.add_xpath("address", '//h1/following-sibling::p[1]/text()')
        
        l.add_xpath("askingPrice", '//div[@data-automation-id = "key" and text() = "Pris"]/following-sibling::div[@data-automation-id = "value"]/text()', MapCompose(self.normalizeNumber))
        l.add_xpath("askingPrice", '//h1/following-sibling::dl[1]/dd/text()', MapCompose(self.normalizeNumber))
        
        for k, v in numberFields.items():
            xpath = xpathTemplate.format(k)
            l.add_xpath(v, xpath, MapCompose(self.normalizeNumber))

        for k, v in oneWordTextFields.items():
            xpath = xpathTemplate.format(k)
            l.add_xpath(v, xpath, MapCompose(self.normalizeOneWordValue))

        yield l.load_item()






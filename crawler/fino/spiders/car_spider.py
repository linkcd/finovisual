# -*- coding: utf-8 -*-

import scrapy
import pdb
import time
import datetime

from scrapy.loader.processors import MapCompose

from fino.spiders.spiderhelper import SpiderHelper
from fino.items import CarItem 
from fino.itemloaders import CarItemLoader


class CarSpider(scrapy.Spider):
    name = "car"
    start_urls = ["http://m.finn.no/car/used/search.html?make=0.813&make=0.817&model=1.813.2000062&model=1.817.1433"]

    def parse(self, response):
        for url in response.xpath("//div[@class='flex-unit']/a/@href").extract():
            follow_url = "http://m.finn.no" + url
            yield scrapy.Request(follow_url, self.parse_car_page)

    def parse_car_page(self, response):
        item = CarItem()

        item["url"] = response.url
        item["finnCode"] = SpiderHelper.getCodeFromRawUrl(response.url)
        item["crawlTime"] = datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S") 

        l = CarItemLoader(item = item, response = response)
        
        l.add_xpath("model", '//h1/text()', MapCompose(SpiderHelper.normalizeOneWordValue))
        l.add_xpath("title", '//h1/following-sibling::p[1]/text()')
        l.add_xpath("price", '//div[@data-automation-id = "key" and text() = "Totalpris"]/following-sibling::div[@data-automation-id = "value"]/text()', MapCompose(SpiderHelper.normalizeNumber))

        numberFields = {  "Omregistrering": "purcharseFee",\
                          "rsmodell": "modelYear",\
                          "Antall eiere": "previousOwners",\
                          "Km.stand": "mileage"}

        textFields = { "1. gang registrert":"firstTimeRegister" , \
                          "rsavgift":"annualfeeincluded", \
                          "Girkasse":"gearType",  \
                          "Drivstoff":"fuelType",  \
                          "Salgsform":"saleForm",  \
                          "Reg.nr.":"RegNumber"  }

        xpathTemplate = "//h1/following-sibling::dl/dt[@data-automation-id='key' and contains(text(), '{0}')]/following-sibling::dd[1]/text()"
        

        for k, v in numberFields.items():
            xpath = xpathTemplate.format(k)
            l.add_xpath(v, xpath, MapCompose(SpiderHelper.normalizeNumber)) 
        for k, v in textFields.items():
            xpath = xpathTemplate.format(k)
            l.add_xpath(v, xpath)


        EUcheckURL = response.xpath('//a[text() = "Sjekk tid for neste EU-kontroll"]/@href').extract()

#TODO: cannot pass capcha check, ignore EUCheckULR now
        EUcheckURL = None
#End of TODO
        if not EUcheckURL:
            #do nothing, return that we have
            yield l.load_item()
        else:
            #get extra EU control info, passing the item loader to that request, and let the new parser handle and return the item 
            yield scrapy.Request(EUcheckURL[0], self.parse_EUControl_Info, meta={'loader':l}) 
            

    def parse_EUControl_Info(self, response):
        l = response.meta['loader']
        


        l.add_value('lastEUControl', 123123123123131321123123123123213)
        yield l.load_item()

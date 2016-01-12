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
    domain = "http://m.finn.no"
        
    areas = {
        "Akershus":"20003",\
        "Aust-Agder":"20010",\
        "Buskerud":"20007",\
        "Finnmark":"20020",\
        "Hedmark":"20005",\
        "Hordaland":"20013",\
        "Møre og Romsdal":"20015",\
        "Nord-Trøndelag":"20017",\
        "Nordland":"20018",\
        "Oppland":"20006",\
        "Oslo":"20061",\
        "Rogaland":"20012",\
        "Sogn og Fjordane":"20014",\
        "Sør-Trøndelag":"20016",\
        "Telemark":"20009",\
        "Troms":"20019",\
        "Vest-Agder":"20011",\
        "Vestfold":"20008",\
        "Østfold":"20002" }

    name = "car"
    #start_urls = [domain + "/car/used/search.html?make=0.813&make=0.817&model=1.813.2000062&model=1.817.1433"] #all Golf and Auris
    start_urls = [domain + "/car/used/search.html?make=0.744&make=0.808&make=0.817&model=1.744.2000166&model=1.744.2046&model=1.808.1355&model=1.817.1437"]

    def parse(self, response):
        for url in response.xpath("//div[@class='flex-unit']/a/@href").extract():
            follow_url = "http://m.finn.no" + url
            yield scrapy.Request(follow_url, self.parse_car_page)
        
        next_page_url = response.xpath('//a[@rel = "next"]/@href').extract() 
        if not not next_page_url:
            yield scrapy.Request(self.domain + next_page_url[0], self.parse)
    

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

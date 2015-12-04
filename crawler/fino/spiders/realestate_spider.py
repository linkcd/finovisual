# -*- coding: utf-8 -*-

import scrapy
import pdb
from fino.items import RealEstateItem 
from fino.itemloaders import RealEstateItemLoader
from scrapy.loader.processors import MapCompose

class RealEstateSpider(scrapy.Spider):
    name = "realEstate"
    start_urls = ["http://www.finn.no/finn/realestate/homes/result?areaId=20045"]
    mobile_version_url_template = "http://m.finn.no/realestate/homes/ad.html?finnkode="

    @staticmethod
    def getCodeFromRawUrl(rawURL):
        from urlparse import urlsplit
        url_data = urlsplit(rawURL)
        from urlparse import parse_qs
        qs_data = parse_qs(url_data.query)
        return qs_data["finnkode"][0]

    @staticmethod
    def normalizeNumber(number):
        toremove = dict.fromkeys((ord(c) for c in u'\xa0mn\xb2\n\t \,\-'))
        return number.translate(toremove)

    @staticmethod
    def normalizeOneWordValue(rawOneWordValue):
        toremove = dict.fromkeys((ord(c) for c in u'\n '))
        return rawOneWordValue.translate(toremove)

    def parse(self, response):
        for url in response.xpath('//div[@class="fright objectinfo"]/div/h2/a/@href').extract():
            #get the mobile version url
            code = self.getCodeFromRawUrl(url) 
            mobile_version_url = self.mobile_version_url_template + code 
            
            yield scrapy.Request(mobile_version_url, self.parse_realEstate_page)

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

        item["finnCode"] = self.getCodeFromRawUrl(response.url)
        l = RealEstateItemLoader(item = item, response = response)
        l.add_xpath("title", '//h1/text()')
        l.add_xpath("address", '//h1/following-sibling::p[1]/text()')
        l.add_xpath("askingPrice", '//h1/following-sibling::dl[1]/dd/text()', MapCompose(self.normalizeNumber))

        for k, v in numberFields.items():
            xpath = xpathTemplate.format(k)
            l.add_xpath(v, xpath, MapCompose(self.normalizeNumber))

        for k, v in oneWordTextFields.items():
            xpath = xpathTemplate.format(k)
            l.add_xpath(v, xpath, MapCompose(self.normalizeOneWordValue))

        yield l.load_item()





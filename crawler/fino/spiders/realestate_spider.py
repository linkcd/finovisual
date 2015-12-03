# -*- coding: utf-8 -*-

import scrapy
from fino.items import RealEstateItem
import pdb

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
    def normalizeLetter(word):
        return word.replace("å", "aa").replace("æ", "ae").replace("ø", "o").replace(".", "").replace("/", "_")
    
    @staticmethod
    def normalizePrice(number):
        toremove = dict.fromkeys((ord(c) for c in u'\xa0\n\t \,\-'))
        return number.translate(toremove)

    @staticmethod
    def normalizeSize(number):
        toremove = dict.fromkeys((ord(c) for c in u'\xa0m\xb2\n\t '))
        return number.translate(toremove)

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


        priceFieldList = {  "Verditakst"    : "verditakst", \
                            "Felleskost"    : "felleskost"  }

        areaFieldList =  {  u"Prim"    : "primaerrom", \
                            "Bruksareal"    : "bruksareal", \
                            "Bruttoareal"   : "bruttoareal", \
                            "Tomteareal"    : "tomteareal" }

        integerFieldList = {"Rom": "rom", \
                            "Bygge": "byggeaar", \
                            "Soverom": "soverom"}

        textFieldList = ["Boligtype", "Energimerking", "Eieform"]
                            


        item["finnCode"] = self.getCodeFromRawUrl(response.url)
        item["title"] =  response.xpath('//h1/text()').extract()[0] 
        item["address"] = response.xpath('//h1/following-sibling::p[1]/text()').extract()[0]
        item["askingPrice"] = self.normalizePrice(response.xpath('//h1/following-sibling::dl[1]/dd/text()').extract()[0])

        for k, v in priceFieldList.items():
            xpath = "//h1/following-sibling::dl/dt[@data-automation-id='key' and contains(text(), '{0}')]/following-sibling::dd[1]/text()".format(k)
            value = self.normalizePrice(response.xpath(xpath).extract()[0])
            item[v] = self.normalizePrice(value)

        for k, v in areaFieldList.items():
            xpath = "//h1/following-sibling::dl/dt[@data-automation-id='key' and contains(text(), '{0}')]/following-sibling::dd[1]/text()".format(k)
            item[v] = self.normalizeSize(response.xpath(xpath).extract()[0])

        for k, v in integerFieldList.items():
            xpath = "//h1/following-sibling::dl/dt[@data-automation-id='key' and contains(text(), '{0}')]/following-sibling::dd[1]/text()".format(k)
            item[v] = self.normalizePrice(response.xpath(xpath).extract()[0])

        for x in textFieldList:
            xpath = "//h1/following-sibling::dl/dt[@data-automation-id='key' and contains(text(), '{0}')]/following-sibling::dd[1]/text()".format(x)
            item[x.lower()] = self.normalizePrice(response.xpath(xpath).extract()[0])

        yield item




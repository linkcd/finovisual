# -*- coding: utf-8 -*-

# Define here the models for your items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RealEstateItem(scrapy.Item):
    url = scrapy.Field()
    finnCode = scrapy.Field()
    title = scrapy.Field()
    address = scrapy.Field()

    askingPrice = scrapy.Field()
    verditakst = scrapy.Field()
    laanetakst= scrapy.Field()
    felleskost= scrapy.Field()
    fellesformue= scrapy.Field()

    primaerrom= scrapy.Field()
    bruksareal= scrapy.Field()
    bruttoareal= scrapy.Field()
    soverom= scrapy.Field()
    rom= scrapy.Field()
    etasje = scrapy.Field()
    byggeaar= scrapy.Field()
    tomteareal= scrapy.Field()

    eieform= scrapy.Field()
    boligtype= scrapy.Field()
    energimerking= scrapy.Field()

    latitude = scrapy.Field()
    longitude = scrapy.Field()

    isNewBuilding = scrapy.Field()
    crawlTime = scrapy.Field()


class CarItem(scrapy.Item):
    url = scrapy.Field()
    finnCode = scrapy.Field()
    crawlTime = scrapy.Field()

    model = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    purcharseFee = scrapy.Field()
    annualfeeincluded = scrapy.Field()
    
    modelYear = scrapy.Field()
    firstTimeRegister = scrapy.Field()
    mileage = scrapy.Field()
    gearType = scrapy.Field()
    fuelType = scrapy.Field()
    saleForm = scrapy.Field()
    RegNumber = scrapy.Field()
    previousOwners = scrapy.Field()


    regYear = scrapy.Field()
    regFirstTimeInNorway = scrapy.Field()
    regFirstTimeOwner = scrapy.Field()
    regDistrict = scrapy.Field()
    lastEUControl = scrapy.Field()
    nextEUControl = scrapy.Field()


    

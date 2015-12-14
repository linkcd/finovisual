# -*- coding: utf-8 -*-

# Define here the models for your scraped items
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

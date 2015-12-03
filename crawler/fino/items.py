# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RealEstateItem(scrapy.Item):
    finnCode = scrapy.Field()
    title = scrapy.Field()
    askingPrice = scrapy.Field()
    address = scrapy.Field()
    verditakst = scrapy.Field()
    laanetakst= scrapy.Field()
    fellesformue= scrapy.Field()
    felleskost= scrapy.Field()
    primaerrom= scrapy.Field()
    bruksareal= scrapy.Field()
    soverom= scrapy.Field()
    bruttoareal= scrapy.Field()
    rom= scrapy.Field()
    boligtype= scrapy.Field()
    eieform= scrapy.Field()
    tomteareal= scrapy.Field()
    byggeaar= scrapy.Field()
    energimerking= scrapy.Field()

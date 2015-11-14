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


    Verditakst = scrapy.Field()
    Laanetakst= scrapy.Field()
    Fellesformue= scrapy.Field()
    Felleskost= scrapy.Field()
    Primaerrom= scrapy.Field()
    Bruksareal= scrapy.Field()
    Soverom= scrapy.Field()
    Bruttoareal= scrapy.Field()
    Rom= scrapy.Field()
    Boligtype= scrapy.Field()
    Eieform= scrapy.Field()
    Tomteareal= scrapy.Field()
    Byggeaar= scrapy.Field()
    Energimerking= scrapy.Field()

# -*- coding: utf-8 -*-

from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Identity

class RealEstateItemLoader(ItemLoader):

    default_output_processor = TakeFirst()

    
    





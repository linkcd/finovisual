# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import requests
import logging
import pdb
import os
import yaml

from fino.items import RealEstateItem 
from fino.items import CarItem 

from scrapy.exceptions import DropItem
from scrapy.utils.serialize import ScrapyJSONEncoder
encoder = ScrapyJSONEncoder()

from geopy.geocoders import Nominatim, GoogleV3

class AzureStorageItemPipeline(object):

    keyFileName = os.path.join(os.path.dirname(__file__), 'keys.key')
    filestream = open(keyFileName, "r")
    keys = yaml.load(filestream)
    headers = {'Content-Type': 'application/json', 'X-API-Key':keys["WebAPIKey"]}

    def postToWebService(self, item, url):
        #http post
        data=encoder.encode(item)
        r = requests.post(url, data, headers = self.headers)
        

    def process_item(self, item, spider):
        if type(item) is RealEstateItem:
            self.handle_realEstate(item)
        if type(item) is CarItem:
            self.handle_car(item)
        return item


    def handle_car(self, item):
        pass


    def handle_realEstate(self, item):
        if item['askingPrice']:

            #geo code
            geolocator = GoogleV3(api_key=self.keys["GoogleGeoAPIKey"])
            location = geolocator.geocode(item["address"])
            if location:
                item["latitude"] = location[1][0]
                item["longitude"] = location[1][1]
#            else:
#                pdb.set_trace()

            url = "http://finovisualization.azurewebsites.net/api/RealEstates"

            self.postToWebService(item, url)
        else:
            pdb.set_trace()
            raise DropItem("Missing price in %s" % item)

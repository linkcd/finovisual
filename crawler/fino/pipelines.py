# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import requests
import logging
import pdb
import os

from scrapy.exceptions import DropItem
from scrapy.utils.serialize import ScrapyJSONEncoder
encoder = ScrapyJSONEncoder()

from geopy.geocoders import Nominatim, GoogleV3

class AzureStorageItemPipeline(object):

    ws_url = "http://finovisualization.azurewebsites.net/api/RealEstates"
    headers = {'Content-Type': 'application/json'}
    key = None
    keyFileName = os.path.join(os.path.dirname(__file__), 'googleGeoAPI.key')

    with open(keyFileName, "r") as keyFile:
        key = keyFile.read().replace('\n', '')

    def process_item(self, item, spider):
        if item['askingPrice']:

            #geo code
            geolocator = GoogleV3(api_key=self.key)
            location = geolocator.geocode(item["address"])
            if location:
                item["latitude"] = location[1][0]
                item["longitude"] = location[1][1]
            else:
                pdb.set_trace()

            #http post
            data=encoder.encode(item)
            r = requests.post(self.ws_url, data, headers = self.headers)

            return item
        else:
            raise DropItem("Missing price in %s" % item)

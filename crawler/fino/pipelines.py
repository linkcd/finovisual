# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import requests
import json
from scrapy.exceptions import DropItem
import logging

from scrapy.utils.serialize import ScrapyJSONEncoder
_encoder = ScrapyJSONEncoder()

import pdb

class AzureStorageItemPipeline(object):

    ws_url = "http://finovisualization.azurewebsites.net/api/RealEstates"
    headers = {'Content-Type': 'application/json'}

    def process_item(self, item, spider):
        if item['askingPrice']:
            data=_encoder.encode(item)
            #r = requests.post(self.ws_url, data, headers = self.headers)
            
            pdb.set_trace()

            return item
        else:
            pdb.set_trace()
            raise DropItem("Missing price in %s" % item)

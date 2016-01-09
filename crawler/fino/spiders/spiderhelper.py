# -*- coding: utf-8 -*-
import re
class SpiderHelper:

    @staticmethod
    def getCodeFromRawUrl(rawUrl):
        #get finncode
        from urlparse import urlsplit
        url_data = urlsplit(rawUrl)
        from urlparse import parse_qs
        qs_data = parse_qs(url_data.query)
        return qs_data["finnkode"][0]

    @staticmethod
    def normalizeNumber(number):
        result = "".join(re.findall('\d+', number.replace(" ", "")))
        if result.isdigit():
            return result
        else:
            return None

    @staticmethod
    def normalizeOneWordValue(rawOneWordValue):
        toremove = dict.fromkeys((ord(c) for c in u'\n '))
        return rawOneWordValue.translate(toremove)

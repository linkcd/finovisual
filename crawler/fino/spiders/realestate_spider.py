import scrapy
from fino.items import RealEstateItem

class RealEstateSpider(scrapy.Spider):
    name = "realEstate"
    start_urls = ["http://www.finn.no/finn/realestate/homes/result?areaId=20045"]

    def parse(self, response):
        for url in response.xpath('//div[@class="fright objectinfo"]/div/h2/a/@href').extract():
            yield scrapy.Request(url, self.parse_realEstate_page)

    def parse_realEstate_page(self, response):
        #from scrapy.shell import inspect_response
        #inspect_response(response, self)
        item = RealEstateItem()

        #code
        from urlparse import urlsplit
        url_data = urlsplit(response.url)
        from urlparse import parse_qs
        qs_data = parse_qs(url_data.query)
        item["finnCode"] = qs_data["finnkode"]

        #item["askingPrice"] = response.xpath('//div[@class="bd objectinfo" and @data-automation-id="information"]/div[@class="line r-cols1to2"]/div[@class="unit"]/dl[@class="multicol"]/dt').extract_first()
        yield item




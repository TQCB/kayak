# Import libraries
import logging
import scrapy
from scrapy.crawler import CrawlerProcess
import json
import os

# Define path to URLs
path_url = r'C:\Users\rapha\My Drive\Work\jedha_dsfs\coursework\p_kayak_data_collection\data\booking_urls.json'

# Open URL json file
with open(path_url, 'r') as file:
    urls = json.load(file)

# Create list only containing URLs
url_list = [d['url'] for d in urls]

class BookingDataSpider(scrapy.Spider):
    name = 'booking_data'
    start_urls = url_list
    
    def parse(self, response):
        
        yield {
            'url'              : response.url,
            'hotel_name'    : response.xpath('/html/body/div[4]/div/div[5]/div[1]/div[1]/div[1]/div[1]/div[2]/div[4]/div[1]/div/div/h2/text()').get(),
            'hotel_name_alt'    : response.xpath('/html/body/div[4]/div/div[4]/div[1]/div[1]/div[1]/div[1]/div[2]/div[4]/div[1]/div/div/h2/text()').get(),
            'address'       : response.xpath('/html/body/div[4]/div/div[5]/div[1]/div[1]/div[1]/div[1]/div[2]/div[4]/p/span[1]/text()').get(),
            'address_alt'       : response.xpath('/html/body/div[4]/div/div[4]/div[1]/div[1]/div[1]/div[1]/div[2]/div[4]/p/span[1]/text()').get(),
            'rating'        : response.xpath('/html/body/div[4]/div/div[5]/div[1]/div[1]/div[1]/div[1]/div[4]/div/div[1]/div[1]/div/div[1]/a/div/div/div/div[1]/text()').get(),
            'rating_alt'        : response.xpath('/html/body/div[4]/div/div[4]/div[1]/div[1]/div[1]/div[1]/div[4]/div/div[1]/div[1]/div/div[1]/a/div/div/div/div[1]/text()').get(),
            'rating_amount' : response.xpath('/html/body/div[4]/div/div[5]/div[1]/div[1]/div[1]/div[1]/div[4]/div/div[1]/div[1]/div/div[1]/a/div/div/div/div[2]/div[2]/text()').get(),
            'rating_amount_alt' : response.xpath('/html/body/div[4]/div/div[4]/div[1]/div[1]/div[1]/div[1]/div[4]/div/div[1]/div[1]/div/div[1]/a/div/div/div/div[2]/div[2]/text()').get(),
            # 'coordinates'      : response.xpath('/html/body/div[4]/div/div[5]/div[1]/div[1]/div[1]/div[1]/div[4]/div/div[2]/div/a/div/div').attrib['style'],
        }
        
filenamepath = r'C:\Users\rapha\My Drive\Work\jedha_dsfs\coursework\p_kayak_data_collection\data\booking_data.json'

process_data = CrawlerProcess(settings= {
    'USER_AGENT': 'Chrome/123.0.0.0',
    'LOG_LEVEL': logging.INFO,
    "FEEDS": {
        filenamepath : {"format": "json", 'overwrite' : True},
    }
})

process_data.crawl(BookingDataSpider)
process_data.start()
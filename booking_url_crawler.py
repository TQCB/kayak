# Import libraries
import logging
import scrapy
from scrapy.crawler import CrawlerProcess
import pandas as pd
import os

# Create list of cities
path_cities = r'C:\Users\rapha\My Drive\Work\jedha_dsfs\coursework\p_kayak_data_collection\data\best_5_cities.csv'

cities = pd.read_csv(path_cities)
cities = cities.iloc[:,0].tolist()


# Define new spider inheriting base scrapy spider Class
class BookingURLSpider(scrapy.Spider):

    # Spider name
    name = "booking_urls"

    # Spider URLs to start crawl from
    start_urls = ['https://www.booking.com/searchresults.fr.html?ss={}&checkin=2024-04-02&checkout=2024-04-05&group_adults=2&no_rooms=1&group_children=0'.format(city)
                  for city in cities]

    # Parsing and iteration across links with little spidey boi
    def parse(self, response):
        city = response.url.split('=')[1].split('&')[0]          # extract city name from requested URL
        for i in range(20):                                      # pull first 20
            properties = response.xpath('//div[@data-testid="property-card"][{}]'.format(i))
            for property in properties:                          # for every card, get name and link
                yield {
                    'city' : city,
                    'url' : property.xpath('div[1]/div[2]/div/div[1]/div[1]/div/div[1]/div/h3/a').attrib['href']
                }

filenamepath = r'C:\Users\rapha\My Drive\Work\jedha_dsfs\coursework\p_kayak_data_collection\data\booking_urls.json'

# Define new crawler process
process_url = CrawlerProcess(settings = {
    'USER_AGENT': 'Chrome/123.0.0.0',
    'LOG_LEVEL': logging.INFO,
    "FEEDS": {
        filenamepath : {"format": "json", 'overwrite' : True},
    }
})

# Start the crawling with spider
process_url.crawl(BookingURLSpider)
process_url.start()
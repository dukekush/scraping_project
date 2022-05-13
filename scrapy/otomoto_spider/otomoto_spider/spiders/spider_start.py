# -*- coding: utf-8 -*-
import scrapy

class Link(scrapy.Item):
    link = scrapy.Field()

class LinkListsSpider(scrapy.Spider):
    name = 'link_lists'
    allowed_domains = ['www.otomoto.pl']

    start_urls = ['https://www.otomoto.pl/osobowe/seg-cabrio']

    #  scraping pages for the next step
    def parse(self, response):
        xpath = '//*[@id="__next"]/div/div/div/div[2]/div[2]/div[2]/div[1]/div[3]/div[4]/ul/li[last()-1]/a/span/text()'
        total_pages = response.xpath(xpath).get()  # number of pages - at the bottom of the start url
        print(total_pages, type(total_pages))      # check if working correctly
        for n in range(1, int(total_pages) + 1):
            l = Link()
            l['link'] = 'https://www.otomoto.pl/osobowe/seg-cabrio?page={}'.format(n)  
            yield l
    


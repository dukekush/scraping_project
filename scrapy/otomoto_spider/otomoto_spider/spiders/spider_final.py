import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re


# set variable below to True to limit crawler to scrape about 100 offers (limits crawler to first 4 numbered pages)
LIMIT_ITEMS = True


#  class for saving results of crawler
class Car(scrapy.Item):
    price   = scrapy.Field()
    make    = scrapy.Field()
    model   = scrapy.Field()
    year    = scrapy.Field()
    km      = scrapy.Field()
    power   = scrapy.Field()
    color   = scrapy.Field()
    fuel    = scrapy.Field()
    cap     = scrapy.Field()
    trans   = scrapy.Field()
    drive   = scrapy.Field()


class LinksSpider(CrawlSpider):
    name = 'cars'
    allowed_domains = ['www.otomoto.pl']

    # retrieving links pages to scrape
    try:
        with open("data/links.csv", "rt") as f:
            if LIMIT_ITEMS:
                start_urls = [url.strip() for url in f.readlines()][1:5]
            else:
                tart_urls = [url.strip() for url in f.readlines()][1:]
    except:
        start_urls = []

    # rule below allows us to follow any link containing words "oferta" from each of start_urls,
    # because of this on each numbered paged crawler will go to many subpages with offers, and the scrape data from them
    rules = (
        Rule(LinkExtractor(allow="oferta"), callback='parse'), 
    )

    # method for scraping data and saving it to scrapy.Item
    def parse(self, response):
        car = Car()

        try:
            car['price']  =  re.sub('\W+', '', response.xpath('//*[@class="offer-price__number"]/text()').get())
        except:
            car['price']  = ''
        try:
            car['make']   =  re.sub('\W+','',response.xpath("//*[contains(text(), 'Marka pojazdu')]/../div/a/text()").get())
        except:
            car['make']   = ''
        try:
            car['model']  =  re.sub('\W+','',response.xpath("//*[contains(text(), 'Model pojazdu')]/../div/a/text()").get())
        except:
            car['model']  = ''
        try:
            car['year']   =  re.sub('\W+','',response.xpath("//*[contains(text(), 'Rok produkcji')]/../div/text()").get())
        except:
            car['year']   = ''
        try:
            car['km']     =  re.sub('\W+','',response.xpath("//*[contains(text(), 'Przebieg')]/../div/text()").get())
        except:
            car['km']     = ''
        try:
            car['power']  =  re.sub('\W+','',response.xpath("//*[contains(text(), 'Moc')]/../div/text()").get())
        except:
            car['power']  = ''
        try:
            car['color']  =  re.sub('\W+','',response.xpath("//*[contains(text(), 'Kolor')]/../div/a/text()").get())
        except:
            car['color']  = ''
        try:
            car['fuel']   =  re.sub('\W+','',response.xpath("//*[contains(text(), 'Rodzaj paliwa')]/../div/a/text()").get())
        except:
            car['fuel']   = ''
        try:
            car['cap']    =  re.sub('\W+','',response.xpath("//*[contains(text(), 'Pojemność skokowa')]/../div/text()").get())
        except:
            car['cap']    = ''
        try:
            car['trans']  =  re.sub('\W+','',response.xpath("//*[contains(text(), 'Skrzynia biegów')]/../div/a/text()").get())
        except:
            car['trans']  = ''
        try:    
            car['drive']  =  re.sub('\W+','',response.xpath("//*[contains(text(), 'Napęd')]/../div/a/text()").get())
        except:
            car['drive']  = ''

        yield car
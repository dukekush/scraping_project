import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re

class Car(scrapy.Item):
    price = scrapy.Field()
    make = scrapy.Field()
    model = scrapy.Field()
    year = scrapy.Field()
    km = scrapy.Field()
    power = scrapy.Field()
    color = scrapy.Field()
    fuel = scrapy.Field()
    cap = scrapy.Field()
    trans = scrapy.Field()
    drive = scrapy.Field()

class LinksSpider(CrawlSpider):
    name = 'cars_final'
    allowed_domains = ['www.otomoto.pl']
    try:
        with open("links.csv", "rt") as f:
            start_urls = [url.strip() for url in f.readlines()][1:]
    except:
        start_urls = []

    print(start_urls)

    rules = (
        Rule(LinkExtractor(allow="oferta"), callback='parse'), 
    )

    def parse(self, response):
        car = Car()
        car['price']  =  re.sub('\W+', '', response.xpath('//*[@class="offer-price__number"]/text()').get())
        car['make']   =  re.sub('\W+','',response.xpath("//*[contains(text(), 'Marka pojazdu')]/../div/a/text()").get())
        car['model']  =  re.sub('\W+','',response.xpath("//*[contains(text(), 'Model pojazdu')]/../div/a/text()").get())
        car['year']   =  re.sub('\W+','',response.xpath("//*[contains(text(), 'Rok produkcji')]/../div/text()").get())
        car['km']     =  re.sub('\W+','',response.xpath("//*[contains(text(), 'Przebieg')]/../div/text()").get())
        car['power']  =  re.sub('\W+','',response.xpath("//*[contains(text(), 'Moc')]/../div/text()").get())
        car['color']  =  re.sub('\W+','',response.xpath("//*[contains(text(), 'Kolor')]/../div/a/text()").get())
        car['fuel']   =  re.sub('\W+','',response.xpath("//*[contains(text(), 'Rodzaj paliwa')]/../div/a/text()").get())
        car['cap']    =  re.sub('\W+','',response.xpath("//*[contains(text(), 'Pojemność skokowa')]/../div/text()").get())
        car['trans']  =  re.sub('\W+','',response.xpath("//*[contains(text(), 'Skrzynia biegów')]/../div/a/text()").get())
        car['drive']  =  re.sub('\W+','',response.xpath("//*[contains(text(), 'Napęd')]/../div/a/text()").get())
        yield car

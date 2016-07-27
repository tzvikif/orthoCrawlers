import scrapy

class AngleItem(scrapy.Item):
    title = scrapy.Field()
    voldate = scrapy.Field()
    abstract = scrapy.Field()
import scrapy

class AjoItem(scrapy.Item):
    title = scrapy.Field()
    voldate = scrapy.Field()
    abstract = scrapy.Field()
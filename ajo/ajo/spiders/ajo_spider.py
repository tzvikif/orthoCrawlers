import scrapy
import os
from urlparse import urlparse

from ajo.items import AjoItem

class AjoSpider(scrapy.Spider):
    name = "ajo"
    allowed_domains = ["ajodo.org"]
    start_urls = [
      "http://www.ajodo.org/issue/S0889-5406(13)X0018-6",
    #    "http://www.ajodo.org/issue/S0889-5406(13)X0017-4",
    #    "http://www.ajodo.org/issue/S0889-5406(13)X0007-1",
    ]
    def parse(self, response):
        self.count = 0
        href = response.xpath('//noscript/a/@href').extract()
      	if not href:
      	    print "*"*50
      	    print response.body
      	    return	
        url = urlparse(href[0])
        
        #print url
        request = scrapy.Request(url.geturl(), callback=self.parse_articles_contents)
        yield request
        return
        for index,sel in enumerate(root):
            #item = EjoItem()
            #item['voldate'] = voldate
            #self.item['title'] = sel.xpath('div[1]/@title').extract()
            #print self.item['title']
            href = sel.xpath('.//a[@title="Abstract"]/@href | .//a[@title="Extract"]/@href' ).extract()
            url = response.urljoin(href[0])
            #yield item
            request = scrapy.Request(url, callback=self.parse_dir_contents)
            request.meta['voldate'] = voldate
            #desc = sel.xpath('//div[@abstract').extract()
            #print index,href,url
            yield request
        
    def parse_articles_contents(self, response):
        articles = response.xpath('//div[@class="articleCitation"]')
        
        for index,article in enumerate(articles):
            #print index,article.extract()
            published = article.xpath('.//div[@class="published-online"]/text()').extract()
            title = article.xpath('.//h3/a/text()').extract()
            href = article.xpath('.//div[@class="formats"]//a[contains(@href,"fulltext")]/@href').extract()
            
            if  href:
                url = response.urljoin(href[0])
                request = scrapy.Request(url, callback=self.parse_abstract_contents1)
                request.meta['published'] = published
                request.meta['title'] = title
                yield request
		
    def parse_abstract_contents1(self, response):
        item = AjoItem()
        #href = response.xpath('//noscript/a/@href').extract()
        abstract = response.xpath('//div[@class="abstract"]//text()').extract()
        voldate = response.xpath('//div[@class="artBib"]//text()').extract()
        voldateStr = ' '.join(voldate)
        if	not abstract:
            return
        published = response.meta['published']
        title = response.meta['title']
        self.count = self.count + 1
        origDirectory = baseDirectory = os.getcwd()
        print baseDirectory
        dir = published[0].split(': ')[1].strip().replace(' ','_')    
        currentDirectory = "/" + dir
        fullDirectory = baseDirectory+currentDirectory
        if not os.path.exists(fullDirectory):
            os.mkdir(fullDirectory)
        os.chdir(fullDirectory)
        #fname = response.url[38:-9]
        #fname = fname.replace('/','.')
        #fname = fname + '.txt'
        fname = 'test%d.txt'%self.count
        with open(fname, "wb") as f:
       	    f.write(voldateStr.encode('utf8'))
       	    f.write('\n'.encode('utf8'))
       	    f.write(('-'*50).encode('utf8'))
       	    f.write('\n'.encode('utf8'))
            f.write(title[0].encode('utf8'))
            f.write('\n'.encode('utf8'))
            f.write(('-'*50).encode('utf8'))
            f.write('\n'.encode('utf8'))
            for i,txt in enumerate(abstract):    
                f.write(abstract[i].encode('utf8'))
                f.write('\n'.encode('utf8'))
        f.close()
        os.chdir(origDirectory)
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		

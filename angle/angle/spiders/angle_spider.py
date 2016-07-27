import scrapy
import os
from urlparse import urlparse

from angle.items import AngleItem

class AngleSpider(scrapy.Spider):
    name = "angle"
    allowed_domains = ["angle.org"]
    start_urls = [
    "http://www.angle.org/toc/angl/85/4",
    ]
    def parse(self, response):
        self.count = 0
        articles = response.xpath('//table[@class="articleEntry"]')
        print '*'*50
        #print articles
        for index,article in enumerate(articles):
            href = article.xpath('.//a[text()="Abstract"]/@href').extract()
            if href:
                url = response.urljoin(href[0])
                request = scrapy.Request(url, callback=self.parse_dir_contents)
                yield request
              
    def parse_dir_contents(self, response):
        articleHeading = response.xpath('//div[@id="articleToolsHeading"]//text()').extract()
        articleCitation = response.xpath('//div[@class="articleMeta"]//text()').extract()
        title = response.xpath('//div[@class="art_title"]/text()').extract()
        abstract = response.xpath('//div[@class="abstractSection"]//text()').extract()
        self.count = self.count + 1
        origDirectory = baseDirectory = os.getcwd()
        #print "*"*50
        articleCitationStr = ''.join(articleCitation)
        #print articleCitationStr
        dir = articleHeading[1] + articleHeading[2]
        dir = dir.strip().replace(' ','_')
        dir = dir.replace(',','')
        currentDirectory = "/" + dir
        fullDirectory = baseDirectory+currentDirectory
        if not os.path.exists(fullDirectory):
            os.mkdir(fullDirectory)
        os.chdir(fullDirectory)
        #fname = response.url[38:-9]
        #fname = fname.replace('/','.')
        #fname = fname + '.txt'
        #fname = 'test%d.txt'%self.count
     	with open(fname, "wb") as f:
       	    f.write(articleHeading[1].encode('utf8'))
       	    f.write(articleHeading[2].encode('utf8'))
       	    f.write('\n'.encode('utf8'))
       	    f.write(articleCitationStr.encode('utf8'))
       	    f.write('\n'.encode('utf8'))
            f.write(title[0].encode('utf8'))
            f.write('\n'.encode('utf8'))
            f.write(('-'*50).encode('utf8'))
            f.write('\n'.encode('utf8'))
            for i,txt in enumerate(abstract):    
                f.write(abstract[i].encode('utf8'))
        f.close()
        os.chdir(origDirectory)
        
 
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		

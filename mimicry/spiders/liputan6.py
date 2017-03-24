import scrapy
import time
import re
import random

class liputan6spider(scrapy.Spider):
    name = "liputan6"
    filename="mimicry.csv"
    categories = ["News"]
    tag = ["jakarta","bandung","semarang"]
    reporter = ["Luqman Rimadi"]
    editor = ["Sugeng Triono"]

    def start_requests(self):
        urls = [
            'http://www.liputan6.com',
        ]

        for url in urls:
            yield scrapy.Request(url=url,callback=self.parse)

    def parse(self,response):
        with open(self.filename,  'wb') as f:
            f.write("%s;%s;%s;%s;%s;%s;%s" %("Title","Body Article","Short Desc	","Categories","Tag","Reporter","Editor"))
            f.close()
        news_link = response.css('.articles--iridescent-list--text-item__title')
        for i in range(0,3):
            url = str(news_link.css('a::attr(href)')[i].extract().encode('utf-8'))
            if url is not None:
                yield scrapy.Request(url=url,callback=self.parseContent)


    def parseContent(self,response):
        newline = re.compile("\n|\r|(<b>(Liputan6|Bola|Bintang)\.com, ([a-zA-Z]+(?:[\s-][a-zA-Z]+)*)(</b>| -</b>))")
        with open(self.filename,  'ab') as f:
            f.write("\n%s;%s;%s;%s;%s;%s;%s" %(response.css("h1.read-page--header--title::text").extract_first().encode('utf-8').replace(';',''),
            re.sub(newline,'',response.css("div.article-content-body__item-content").extract_first().encode('utf-8')),
            # response.css("div.article-content-body__item-content").extract_first().encode('utf-8'),
            response.css("meta[name='description']::attr(content)").extract_first().encode('utf-8').replace(';',''),
            random.choice(self.categories),
            random.choice(self.tag),
            random.choice(self.reporter),
            random.choice(self.editor)
            ))

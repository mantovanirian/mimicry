import scrapy

class liputan6spider(scrapy.Spider):
    name = "liputan6"

    def start_requests(self):
        urls = [
            'http://www.liputan6.com',
        ]

        for url in urls:
            yield scrapy.Request(url=url,callback=self.parse)

    def parse(self,response):
        news_link = response.css('.articles--iridescent-list--text-item__title')
        for i in range(0,3):
            url = str(news_link.css('a::attr(href)')[i].extract().encode('utf-8'))
            if url is not None:
                yield scrapy.Request(url=url,callback=self.parseContent)


    def parseContent(self,response):
        filename = 'title.csv'
        with open(filename,  'ab') as f:
            f.write("%s\n" %(response.css("h1.read-page--header--title::text").extract_first().encode('utf-8')))

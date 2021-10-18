import scrapy
from scrapy.crawler import CrawlerProcess


class Recent_Series(scrapy.Spider):
    name = 'airingSeries'
    start_urls = []

    custom_settings = {
      'CONCURRENT_REQUESTS': 100,
      'CONCURRENT_REQUESTS_PER_DOMAIN': 100,
      'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0'
    }

    def __init__(self, category='', c_type='', **kwargs):
        if self.start_urls != []:
            self.start_urls = []
        self.start_urls.append(f'https://gogoanime.sh/?page={category}')

    

    def parse(self, response):
       length = len(response.xpath("//ul[@class='items']/li").getall())
       for item in range(1, length+1):
           yield{
               'name': response.xpath(f"//ul[@class='items']/li[{item}]//p[1]/a//text()").get(),
               'image': response.xpath(f"//ul[@class='items']/li[{item}]//img//@src").get(),
               'episode': response.xpath(f"//ul[@class='items']/li[{item}]//p[2]//text()").get(),
               'r_link': response.xpath(f"//ul[@class='items']/li[{item}]//p[1]//a//@href").get()
               
           }
       


# if __name__ == '__main__':
#     process = CrawlerProcess()
#     process.crawl(Recent_Series, 1, '')
#     process.start()
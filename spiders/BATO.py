import scrapy
from scrapy.crawler import CrawlerProcess

class Bato(scrapy.Spider):
	name = 'Bato_to'
	# start_urls = ['https://ninemanga.com/', 'https://mangahub.se/', 'https://freecomiconline.me/']
	start_urls = ['https://freecomiconline.me/comic/pure-girl-chunqing-yatou-huolala/chapter-479/']

	custom_settings = {
		'CONCURRENT_REQUESTS': 100,
		'CONCURRENT_REQUESTS_PER_DOMAIN': 100,
		'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0'
	}

	def __init__(self, category='', c_type='', **kwargs):
		# if self.start_urls != []:
		# 	self.start_urls = []
		# self.start_urls.append(category)
		super().__init__(**kwargs)

	def parse(self, response):
		yield{
			# 'Title': response.css('title::text').get()
			'DATA --> ': response.xpath("//div[@class='reading-content']/div/img/@src").get().strip()
		}



if __name__ == '__main__':
	process = CrawlerProcess()
	process.crawl(Bato)
	process.start()
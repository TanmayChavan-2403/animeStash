import scrapy
from scrapy.crawler import CrawlerProcess

class mangaC(scrapy.Spider):
	name = 'Mangakakakkalot2'
	start_urls = []

	custom_settings = {
		'CONCURRENT_REQUESTS': 100,
		'CONCURRENT_REQUESTS_PER_DOMAIN': 100,
		'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0'
	}

	def __init__(self, category='', c_type='', **kwargs):
		global _c_type, _category
		_c_type = c_type
		_category = category
		if self.start_urls != []:
			self.start_urls = []
		self.start_urls.append(category)
		super().__init__(**kwargs)

	def parse(self, response):
		page_no = response.xpath("//select[@id='page']/option[1]/text()").get().split('/')[-1]
		for n in range(1, int(page_no) + 1):
			link = _category.split('.html')[0] + f"-{n}" + '.html'
			yield scrapy.Request(link, callback=self.extractImg, meta={'idx': n})
			
	def extractImg(self, response):
		yield{
			response.meta['idx']: response.xpath("//div[@class='pic_box']/img/@src").get()
		}
			



if __name__ == '__main__':
	process = CrawlerProcess()
	process.crawl(mangaC, 'https://ninemanga.com/chapter/GAMERS%21/3386777.html')
	process.start()
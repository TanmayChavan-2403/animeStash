import scrapy
import re
from scrapy.crawler import CrawlerProcess

class gogoPlay(scrapy.Spider):
	name = 'gogoplay'
	start_urls = []

	custom_settings = {
		'CONCURRENT_REQUESTS': 100,
		'CONCURRENT_REQUESTS_PER_DOMAIN': 100,
		'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0'
	}

	def __init__(self, category='', c_type='', **kwargs):
		if self.start_urls != []:
			self.start_urls = []
			
		self.start_urls.append(category)
		super().__init__(**kwargs)


	def parse(self, response):
		d = {}
		q1 = '360p'
		q2 = '480p'
		q3 = '720p'
		q4 = '1080p'
		# idx = int(re.findall('(Episode){1}.(\d*)', response.request.url)[0][-1])
		# size : response.xpath("//span[@id='filesize']//text()").get()
		hlink = ''
		rec = []
		for link in response.css('div.dowload a::attr(href)').getall():
			if q1 in link or q2 in link or q3 in link or q4 in link:
				rec.append(link)
			if 'storage.googleapis' in link:
				hlink = link

		yield {
			'hlink': hlink,
			'links': rec,
			'name': response.xpath(f"//span[@id='title']//text()").get(),
			'size': response.xpath(f"//li[2]//span[@id='filesize']//text()").get(),
			'duration':  response.xpath(f"//span[@id='duration']//text()").get(),
			'resolution': response.xpath(f"//li[4]//span[@id='filesize']//text()").get()
		}


# if __name__ == '__main__':
# 	process = CrawlerProcess()
# 	process.crawl(gogoPlay)
# 	process.start()
import scrapy
import re
from scrapy.crawler import CrawlerProcess

class PopularMangas(scrapy.Spider):
	name = 'popularanimes'
	start_urls = ['https://mangakakalot.com/manga_list?type=topview&category=all&state=all&page=1']
	

	custom_settings = {
		'FEED_URI': 'output.json',
		'CONCURRENT_REQUESTS': 100,
		'CONCURRENT_REQUESTS_PER_DOMAIN': 100,
		'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0'
	}

	def parse(self, response):
		for cnt in response.xpath('//div[@class="truyen-list"]'):
			
			image = cnt.xpath('//div[@class="list-truyen-item-wrap"]/a//img/@src').extract(),
			name = cnt.xpath('//div[@class="list-truyen-item-wrap"]/h3//a/text()').extract(),
			rlink = cnt.xpath('//div[@class="list-truyen-item-wrap"]/a/@href').extract(),
			chapter = cnt.xpath('//div[@class="list-truyen-item-wrap"]/a/text()').extract()
			chapter = [ch for ch in chapter if ch != '\n']

			yield{
				'img': image,
				'name': name,
				'rlink': rlink,
				'chapter': chapter
			}

if __name__ == '__main__':
	process = CrawlerProcess()
	process.crawl(PopularMangas)
	process.start()


import scrapy
import re
from scrapy.crawler import CrawlerProcess

class PopularAnimes(scrapy.Spider):
	name = 'popularanimes'
	start_urls = ['https://mangakakalot.com/manga_list?type=topview&category=all&state=all&page=1',
				'https://gogoanime.pe/']
	

	custom_settings = {
		'FEED_URI': 'output.json',
		'CONCURRENT_REQUESTS': 100,
		'CONCURRENT_REQUESTS_PER_DOMAIN': 100,
		'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0'
	}

	def __init__(self, category='',c_type='', **kwargs):
		
		pass

	def parse(self, response):
		if 'gogoanime' in response.url:
			uls = response.xpath('//ul[@class="items"]')
			n = 0
			for lst in uls:
				n += 1
				rlink = lst.xpath('//li/div[@class="img"]/a/@href').extract()
				img = lst.xpath('//li/div[@class="img"]/a/img/@src').extract()
				names = lst.xpath('//li/p[@class="name"]/a/text()').extract()
				RD = lst.xpath('//li/p[@class="released"]/text()').extract()
				names = [name.strip() for name in names]
				releaseDate = [rd.strip() for rd in RD]
				yield{
					'animeRlink': rlink,
					'animeImg': img,
					'animeName': names,
					'animeReleaseDate': releaseDate
				}
		else:
			for cnt in response.xpath('//div[@class="truyen-list"]'):
				image = cnt.xpath('//div[@class="list-truyen-item-wrap"]/a//img/@src').extract(),
				name = cnt.xpath('//div[@class="list-truyen-item-wrap"]/h3//a/text()').extract(),
				rlink = cnt.xpath('//div[@class="list-truyen-item-wrap"]/a/@href').extract(),
				chapter = cnt.xpath('//div[@class="list-truyen-item-wrap"]/a/text()').extract()
				chapter = [ch for ch in chapter if ch != '\n']

				yield{
					'mangaImg': image,
					'mangaName': name,
					'mangaRlink': rlink,
					'mangaChapter': chapter
				}


if __name__ == '__main__':
	process = CrawlerProcess()
	process.crawl(PopularAnimes)
	process.start()


import scrapy
from scrapy.crawler import CrawlerProcess

class mangaL(scrapy.Spider):
	name = 'Mangakakakkalot2'
	start_urls = []

	custom_settings = {
		'CONCURRENT_REQUESTS': 100,
		'CONCURRENT_REQUESTS_PER_DOMAIN': 100,
		'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0'
	}

	def __init__(self, category, c_type, **kwargs):
		global _c_type, _category
		_c_type = c_type
		_category = category
		if self.start_urls != []:
			self.start_urls = []

		if c_type == 'topview':
			self.start_urls.append(f"https://mangakakalot.com/manga_list?type=topview&category=all&state=all&page={category}")
		elif c_type == 'newest':
			self.start_urls.append(f"https://mangakakalot.com/manga_list?type=newest&category=all&state=all&page={category}")
		elif c_type == 'Completed':
			self.start_urls.append(f"https://mangakakalot.com/manga_list?type=newest&category=all&state=Completed&page={category}")
		else:
			self.start_urls.append('https://mangakakalot.com/')

		super().__init__(**kwargs)

	def parse(self, response):

		if _c_type in ['topview', 'newest', 'Completed']:
			length = len(response.xpath("//div[@class='list-truyen-item-wrap']"))
			for n in range(1, length + 1):
				yield{
					'Image': response.xpath(f"//div[@class='list-truyen-item-wrap'][{n}]/a[1]/img/@src").get(),
					'r_link': response.xpath(f"//div[@class='list-truyen-item-wrap'][{n}]/a[1]/@href").get(),
					'Name': response.xpath(f"//div[@class='list-truyen-item-wrap'][{n}]/h3/a/text()").get(),
					'latest_chap': response.xpath(f"//div[@class='list-truyen-item-wrap'][{n}]/a[2]/text()").get()
				}
			


		else:
			# Popular Manga
			res = []
			for manga in range(1, 21):
				res.append({
						'image': response.xpath(f"//*[@id='owl-demo']/div[{manga}]/img//@src").get(),
						'r_link': response.xpath(f"//*[@id='owl-demo']/div[{manga}]//h3/a/@href").get(),
						'name': response.xpath(f"//*[@id='owl-demo']/div[{manga}]//h3/a/@title").get()
					})
			yield{
				'popular': res
			}

			#Latest manga release
			res = []
			length = len(response.xpath("//div[@class='leftCol']//div[@class='itemupdate first']"))
			for manga in range(1, length+1):
				res.append({
						'image': response.xpath(f"//div[@class='leftCol']//div[@class='itemupdate first'][{manga}]//a//img//@src").get(),
						'name': response.xpath(f"//div[@class='leftCol']//div[@class='itemupdate first'][{manga}]/ul/li[1]/h3/a/text()").get(),
						'r_link': response.xpath(f"//div[@class='leftCol']//div[@class='itemupdate first'][{manga}]/ul/li[1]/h3/a/@href").get(),
						'latest_chap': response.xpath(f"//div[@class='leftCol']//div[@class='itemupdate first'][{manga}]/ul/li[2]/span//@title").get()
					})
			yield{
				'latest': res
			}

if __name__ == '__main__':
	process = CrawlerProcess()
	process.crawl(mangaL, '1', 'Completed')
	process.start()
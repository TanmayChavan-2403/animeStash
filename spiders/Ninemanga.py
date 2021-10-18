import scrapy
from scrapy.crawler import CrawlerProcess

class NineManga(scrapy.Spider):
	name = 'ninemanga'
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
		if c_type == 'dlist':
			baseURL = 'https://ninemanga.com/search/?wd='
			category = category.replace(' ','+').lower()
			self.start_urls.append(baseURL + category)
		else:
			category += '?waring=1'
			self.start_urls.append(category)


		super().__init__(**kwargs)

	def parse(self, response):
		if _c_type == 'dlist':
			# Search results
			length = len(response.xpath("//div[@class='leftbox']//ul[@class='direlist']/li").getall())
			for n in range(1, length + 1):
				yield{
					'Image':  response.xpath(f"//ul[@class='direlist']/li[{n}]//dl[@class='bookinfo']/dt/a/img/@src").get(),
					'r_link': response.xpath(f"//ul[@class='direlist']/li[{n}]//dl[@class='bookinfo']/dd/a/@href").get(),
					'Name': response.xpath(f"//ul[@class='direlist']/li[{n}]//dl[@class='bookinfo']/dd/a/text()").get(),
					'latest_chap': response.xpath(f"//ul[@class='direlist']/li[{n}]//dl[@class='bookinfo']/dd/a[2]/text()").get()
				}
		else:
			#Details 
			status = response.xpath(f"//ul[@class='message']/li[6]/a[1]/text()").get()
			if status is not None:
				status = status.strip()
			else:
				status = ''
			yield{
				'name': response.xpath(f"//ul[@class='message']/li[1]/span/text()").get(),
				'author': response.xpath(f"//ul[@class='message']/li[4]/a/text()").get(),
				'status': status,
				'genres': response.xpath(f"//ul[@class='message']/li[3]/a/text()").getall(),
				'synopsis': response.xpath(f"//p[@itemprop='description']/text()").getall(),
				'year': response.xpath(f"//ul[@class='message']/li[5]/a/text()").get()
			}

			
			# Chapters list

			div_length = len(response.xpath("//div[@class='chapterbox']/div[@class='silde']/ul[@class='sub_vol_ul']"))
			results = []
			for d in range(1, div_length + 1):
				length = len(response.xpath(f"//div[@class='chapterbox']/div[@class='silde']/ul[@class='sub_vol_ul'][{d}]/li"))
				for n in range(1, length + 1 ):

					results.append({
						'title': response.xpath(f"//div[@class='chapterbox']/div[@class='silde']/ul[@class='sub_vol_ul'][{d}]/li[{n}]/a/text()").get(),
						'r_link': response.xpath(f"//div[@class='chapterbox']/div[@class='silde']/ul[@class='sub_vol_ul'][{d}]/li[{n}]/a/@href").get()
					})
			yield{
				'chapters': results
			}

# if __name__ == '__main__':
# 	process = CrawlerProcess()
# 	process.crawl(NineManga, 'https://ninemanga.com/manga/Creepy+Cat.html', 'dlink')
# 	process.start()
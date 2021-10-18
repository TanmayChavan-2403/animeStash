import scrapy
from scrapy.crawler import CrawlerProcess

class staffs(scrapy.Spider):
	name = 'animePlanet'
	# start_urls = ['https://www.anime-planet.com/people/fumihiko-shimo']
	start_urls = []

	custom_settings = {
		'CONCURRENT_REQUESTS': 100,
		'CONCURRENT_REQUESTS_PER_DOMAIN': 100,
		'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0'
	}

	def __init__(self, category='', c_type='', **kwargs):
		
		if self.start_urls != []:
			self.start_urls = []
		
		self.start_urls.append('https://www.anime-planet.com/people/' + category)		

		super().__init__(**kwargs)


	def parse(self, response):
		
		name = response.xpath("//h1[@itemprop='name']//text()").get()
		image = response.xpath("//div[@class='mainEntry']/img/@src").get()
		text = response.xpath("//div[@class='pure-g entrySynopsis synopsisPeople']//div[@class='pure-1 md-2-3']//text()").getall()
		if 'https' not in image:
			image = 'https://www.anime-planet.com' + image
		
		yield{
			'Name': name,
			'Image': image,
			'Text':''.join(text).replace('\n','')
		}

		#Known for 
		title = response.xpath("//ul[@class='cardDeck cardGrid cardGrid5']/preceding::h3[1]").get()
		length = len(response.xpath("//ul[@class='cardDeck cardGrid cardGrid5']//li"))
		res = []
		for n in range(1, length+1):
			res.append({
				'kfImg': response.xpath(f"//ul[@class='cardDeck cardGrid cardGrid5']//li[{n}]//div[@class='crop']//img//@data-src").get(),
				'kfText': response.xpath(f"//ul[@class='cardDeck cardGrid cardGrid5']//li[{n}]/a//h3//text()").get()
			})
		yield{
			'Known for': res
		}

		#Additional Details
		length = len(response.xpath("//table[@class='pure-table striped expandedDetails']"))
		d = {}
		main_res = []
		for n in range(1, length+1):
			dname = {}
			dname.update({
				'AdTitle': response.xpath(f"//table[@class='pure-table striped expandedDetails'][{n}]/preceding::h3[1]//text()").get()
			})
			trLength = len(response.xpath(f"//table[@class='pure-table striped expandedDetails'][{n}]//tr"))
			d1 = {}
			res = []
			for tr in range(1, trLength+1):
				d1.update({tr:{
					'AdImage': response.xpath(f"//table[@class='pure-table striped expandedDetails'][{n}]//tr[{tr}]//img//@src").get(),
					'AdName': response.xpath(f"//table[@class='pure-table striped expandedDetails'][{n}]//tr[{tr}]//td//b//text()").get()
				}})
				
			res.append(dname)
			res.append(d1)
			main_res.append({'DATA': res})
		yield{
			'Final': main_res
		}


# if __name__ == '__main__':
# 	process = CrawlerProcess()
# 	process.crawl(staffs, category='Tetsurou ARAKI',c_type='')
# 	process.start()
import scrapy
from scrapy.crawler import CrawlerProcess

class AnimePlanet(scrapy.Spider):
	name = 'animePlanet'
	# start_urls = ['https://www.anime-planet.com/characters/shoujo']
	start_urls = []

	custom_settings = {
		'CONCURRENT_REQUESTS': 100,
		'CONCURRENT_REQUESTS_PER_DOMAIN': 100,
		'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0'
	}
	

	def __init__(self, category='',c_type='', **kwargs):
		if self.start_urls != []:
			self.start_urls = []
		if c_type == 'lists':
			baseURL = 'https://www.anime-planet.com/characters/'
			for c in list(set(category['characters'])):
				character = c.lower().replace(' ','-')
				self.start_urls.append(baseURL + character)
		else:
			self.myBaseUrl = category
			self.start_urls.append(self.myBaseUrl)
		super().__init__(**kwargs)
		

	
	def parse(self, response):
		title = response.css('title::text').get()
		ch_name = response.css('h1::text').get()
		aka_name = response.css('h2::text').get()
		gender = response.xpath('//*[@id="siteContainer"]/section[1]/div[1]//text()').get().replace('\n', '')
		hair_color = response.xpath('//*[@id="siteContainer"]/section[1]/div[2]//text()').get().replace('\nHair Color:', '')
		loved = response.xpath('//*[@id="siteContainer"]/section[1]/div[3]/a//text()').get()
		hated = response.xpath('//*[@id="siteContainer"]/section[1]/div[4]/a//text()').get()
		image = response.xpath('//img[@class="screenshots"]//@src').get()
		role_anime = response.xpath("//table[@class='pure-table striped noHeader'][1]//td[1]//text()").getall()
		role_position = response.xpath("//table[@class='pure-table striped noHeader'][1]//td[2]//text()").getall()
			
		if 	'https:' not in image:
			image = 'https://www.anime-planet.com' + image

		yield{
			"Title": title,
			'Character name': ch_name,
			'Aka-name': aka_name,
			'Gender': gender,
			'Hair color': hair_color,
			'Loved' : loved,
			'Hated': hated,
			'Image':  image,
			'Roles': list(zip(role_anime, role_position))
		}	

# if __name__ == '__main__':
# 	process = CrawlerProcess()
# 	process.crawl(AnimePlanet)
# 	process.start()
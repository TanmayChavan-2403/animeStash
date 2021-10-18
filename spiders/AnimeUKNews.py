import scrapy
from scrapy.crawler import CrawlerProcess

class AnimeUkNews(scrapy.Spider):
	name = 'reviewspider'
	start_urls = []


	custom_settings = {
		'CONCURRENT_REQUESTS': 100,
		'CONCURRENT_REQUESTS_PER_DOMAIN': 100,
		'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0'
	}

	def __init__(self, category='',c_type='', **kwargs):
		global crawl_type
		crawl_type = c_type

		if self.start_urls != []:
			self.start_urls = []
		self.myBaseUrl = category
		self.start_urls.append(self.myBaseUrl)
		super().__init__(**kwargs)

	# list of news, ect
	def parse(self, response):
		print('Crawl type received is ->', crawl_type)
		if crawl_type == 'list':
			articles = response.xpath('//article')
			for article in articles:
				h_link = article.xpath('div[2]/h2/a/@href').get()
				h_text = article.xpath('div[2]/h2/a//text()').get()
				img_link = article.xpath('div[2]/div/div[1]/a/img/@src').get()
				synopsis = article.xpath('div[2]/div/div[2]//text()').get()

				h_text = h_text.strip().replace('\n', '')

				yield{
					'h_text': h_text,
					'h_link': h_link,
					'Image': img_link,
					'Synopsis': synopsis
				}
		else:
			yield scrapy.Request(response.request.url,  callback = self.parse_dir_contents)

	#Extracting info without all images
	# def parse_dir_contents(self, response): #Anime uk news
		# value = response.xpath("//div[@class='c-post__text']//p//text()").getall()
		# images = response.xpath("//div[@class='c-post__text']//@src").getall()
		# p_img = response.xpath("//div[@class='c-post__featured-image']/img/@src").get()
		# yield{
		# 	'data': ''.join(value).replace('\xa0',''),
		# 	'images' : images,
		# 	'Pst_img': p_img
		# }


	# Extracting info with all images
	def parse_dir_contents(self, response):
		data = response.xpath("//div[@class='c-post__text']//p//text() | //div[@class='c-post__text']//@src ").getall()
		p_image = response.xpath("//div[@class='c-post__featured-image']//img//@src").get()
		string = ''
		res = []
		for value in data:
			if 'https:' not in value:
				string += value
			else:
				res.append({'para': string})
				res.append({'img': value})
				string = ''
		if string != '':
			res.append({'para':string})

		yield{
			'Data': res,
			'Post_image': p_image
		}

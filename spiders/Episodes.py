import scrapy
from scrapy.crawler import CrawlerProcess
import re

class Gogoanime(scrapy.Spider):
	name = 'fetchingspider'
	start_urls = []

	custom_settings = {
		'FEED_URI': 'output.json',
		'CONCURRENT_ITEMS': 200,
		'CONCURRENT_REQUESTS': 100,
		'CONCURRENT_REQUESTS_PER_DOMAIN': 30,
		'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0'
	}

	def __init__(self, category='', c_type='', **kwargs):
		global crawl_type
		crawl_type = c_type

		if self.start_urls != []:
			self.start_urls = []

		if crawl_type == 'dlist':
			category = ' '.join(category.split(' ')[:3])
			self.start_urls.append('https://www2.gogoanime.sh//search.html?keyword={}'.format(category))
		else:
			epi = c_type.split(' ')[-1].strip()
			if f'-episode-{epi}' in category:
				category = category.replace(f'-episode-{epi}', '')
			else:
				category = category.replace('/category','')

			self.myBaseUrl = category
			# epi = c_type.split(' ')[-1]
			for episode in range(1, int(epi)+ 1 ):
				self.start_urls.append('https://www2.gogoanime.sh' + category + f'-episode-{episode}')
			# self.start_urls.append('https://www2.gogoanime.sh' + category)

		super().__init__(**kwargs)


	def parse(self, response):
		if crawl_type == 'dlist':

			data = len(response.xpath("//div[@class='last_episodes']//li"))

			for i in range(1, data+1):
				r_link = response.xpath(f"//div[@class='last_episodes']//li[{i}]//p[@class='name']//@href").get()
				img = response.xpath(f"//div[@class='last_episodes']//li[{i}]//a//img//@src").get()
				text = response.xpath(f"//div[@class='last_episodes']//li[{i}]//p[@class='name']//text()").get()

				r = scrapy.Request('https://gogoanime.sh' + r_link, callback= self.fetch_episodes)
				r.meta['Redirect'] = r_link
				r.meta['Image'] = img
				r.meta['Name'] = text
				yield r
				# yield{
				# 	'Redirect': r_link,
				# 	'Image': img,
				# 	'Name': text
				# }
		else:
			# yield scrapy.Request(response.request.url, callback = self.fetch_links)
			name = int(re.findall("(-episode-)(\d*)", response.request.url)[0][-1])
			yield{
				name : response.xpath("//li[@class='dowloads']/a/@href").get()
			}


	def fetch_episodes(self, response):
		length = len(response.xpath("//ul[@id='episode_page']//li"))
		episodes = response.xpath(f"//ul[@id='episode_page']/li[{length}]/a/text()").get().split('-')[-1]

		yield{
			'Redirect': response.meta['Redirect'],
			'Image': response.meta['Image'],
			'Name': response.meta['Name'],
			'Episodes': episodes
		}

	# def fetch_epi_links(self, response):
	# 	length = len(response.xpath("//ul[@id='episode_page']//li"))
	# 	episodes = response.xpath(f"//ul[@id='episode_page']/li[{length}]/a/text()").get()
		
	# 	for episode in range(1, int(episodes.split('-')[-1])+1  ):
	# 		url = 'https://gogoanime.sh/' + self.myBaseUrl + f'-episode-{episode}'
	# 		yield scrapy.Request(url, callback=self.fetch_links)
	# 	# url = response.css('li.dowloads a::attr(href)').get()
	# 	# yield scrapy.Request(url, callback = self.parse_dir_contents)

	# def fetch_links(self, response):

	# 	url = response.css('li.dowloads a::attr(href)').get()
	# 	yield scrapy.Request(url, callback = self.parse_dir_contents)

	# def parse_dir_contents(self, response):
	# 	d = {}
	# 	q1 = '360p'
	# 	q2 = '480p'
	# 	q3 = '720p'
	# 	q4 = '1080p'
	# 	idx = int(re.findall('(Episode){1}.(\d*)', response.request.url)[0][-1])
	# 	# size : response.xpath("//span[@id='filesize']//text()").get()
	# 	rec = []
	# 	for link in response.css('div.dowload a::attr(href)').getall():
	# 		if q1 in link or q2 in link or q3 in link or q4 in link:
	# 			rec.append(link)
	# 	yield {
	# 		idx: rec
	# 		# 'size': size
	# 	}
	

# if __name__ == '__main__':
# 	process = CrawlerProcess()
# 	process.crawl(Gogoanime, category='/category/bokutachi-wa-benkyou-ga-dekinai', c_type='dlink 13')
# 	process.start()


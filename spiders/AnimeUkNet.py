import scrapy
import re
from scrapy.crawler import CrawlerProcess

class AnimeNews(scrapy.Spider):
	name = 'reviewspider'
	start_urls = []
	# Features -> Latest News, Anime review, manga review, anime figures HL, 
	

	custom_settings = {
		'CONCURRENT_REQUESTS': 100,
		'CONCURRENT_REQUESTS_PER_DOMAIN': 100,
		'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0'
	}

	def __init__(self, category='',c_type='', **kwargs):
		global g_category
		global crawl_type
		g_category = category
		crawl_type = c_type

		if self.start_urls != []:
			self.start_urls = []

		self.start_urls.append(category)
		super().__init__(**kwargs)


############################################################### LATEST NEWS ######################################################	

	def parse(self, response): 
		if 'https://www.uk-anime.net/LatestNews' in g_category:
			img_link = response.xpath("//div[@class='column3b left']//img//@src").getall()
			text = response.xpath("//div[@class='column3b left']//div[3]/a/strong/text() ").getall()
			text_link = response.xpath("//div[@class='column3b left']//div[3]/a//@href").getall()

			for idx in range(len(text)):
				yield{
					'h_text' : text[idx],
					'h_link': 'https://www.uk-anime.net' + text_link[idx],
					'Image': 'https://www.uk-anime.net/' + img_link[idx]
				}
		elif 'Hub-Anime' in g_category or 'Hub-Manga' in g_category or 'Hub-Toy' in g_category:
			baseUrl = 'https://www.uk-anime.net'
			imgURL = response.xpath(" //div[@class='column12 left']//@src ").getall()
			txtURL = response.xpath(" //div[@class='column12 left']//a//text()").getall()
			redURL = response.xpath(" //div[@class='mobilebuffer']//a//@href").getall()
			print(redURL)
			for idx in range(len(imgURL)):
				yield{
					'h_link': 'https://www.uk-anime.net' + redURL[idx],
					'h_text': txtURL[idx],
					'Image': 'https://www.uk-anime.net/' + imgURL[idx]
				}
		elif 'newsitem' in g_category:
			data = response.xpath(f"//div[@id='articlecontent']//text() | //div[@id='articlecontent']/p//img//@src").getall()
			keyword = 'https://www'
			res = []
			for value in data:
				if 'https://www' not in value:
					res.append({'para':value.replace('\r\n','')})
				else:
					res.append({'img': value})
			
			# CODE FOR HTML CONDITIONAL RENDERING
			string = ''
			rec = []
			c = 0
			for data in res:
				if str(list(data)) == "['para']":
					string += data['para']
					c += 1
				if str(list(data)) == "['img']":
					# print(string)
					rec.append({'para': string})
					string = ''
					# print(data['img'])
					rec.append({'img': data['img']})
					c += 1
				if c == 5:
					rec.append({'para': string})
					string = ''
					c = 0
			rec.append({'para': string})

			pst_img = response.xpath("//div[@class='column12 left featuredimage']//img//@src").get()

			yield{
				'Data': rec,
				'Post_image': 'https://www.uk-anime.net' + pst_img
			}

		else:
			data = response.xpath('//div[@class="margin-bottom overflowhide"]//text() | //div[@class="margin-bottom overflowhide"]//img//@src').getall()
			keyword = 'https://www'
			res = []
			for value in data:
				if 'https://www' not in value:
					res.append({'para':value})
				else:
					res.append({'img': value})

			# CODE FOR HTML CONDITIONAL RENDERING
			string = ''
			rec = []
			c = 0
			for data in res:
				if str(list(data)) == "['para']":
					string += data['para']
					c += 1
				if str(list(data)) == "['img']":
					# print(string)
					rec.append({'para': string})
					string = ''
					# print(data['img'])
					rec.append({'img': data['img']})
					c += 1
				if c == 5:
					rec.append({'para': string})
					string = ''
					c = 0
			rec.append({'para': string})

			pst_img = response.xpath("//div[@class='column12 left featuredimage']//img//@src").get()
			# rec.append({'post_image': pst_img})

			yield{
				'Data': rec,
				'Post_image': 'https://www.uk-anime.net' + pst_img
			}

# if __name__ == '__main__':
# 	process = CrawlerProcess()
# 	process.crawl(AnimeNews,'https://www.uk-anime.net/Hub-Anime','details')
# 	process.start()
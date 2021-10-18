import scrapy
import re
from scrapy.crawler import CrawlerProcess

class AnimeNewsNFacts(scrapy.Spider):
	name = 'reviewspider'
	start_urls = []
	# Features -> Latest News, Anime review, manga review, anime figures HL, 
	

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
		if c_type == 'list':
			self.start_urls.append('https://animenewsandfacts.com/category/news/')
		else:
			self.start_urls.append(category)
		super().__init__(**kwargs)

	def parse(self, response):
		if crawl_type == 'list':
			yield{
				'h_link': response.xpath(f"//div[@class='td-big-grid-wrapper']/div[1]/div[1]/a/@href").get(),
				'h_text': response.xpath(f"//div[@class='td-big-grid-wrapper']/div[1]/div[2]//h3/a/text()").get(),
				'Image': response.xpath(f"//div[@class='td-big-grid-wrapper']/div[1]/div[1]/a/img/@src").get()
			}
			length = len(response.xpath(f"//div[@class='td-big-grid-wrapper']/div[2]/div"))
			for div in range(1, length + 1):
				yield{
					'h_link': response.xpath(f"//div[@class='td-big-grid-wrapper']/div[2]/div[{div}]/div[@class='td-module-thumb']//a/@href").get(),
					'h_text': response.xpath(f"//div[@class='td-big-grid-wrapper']/div[2]/div[{div}]/div[@class='td-meta-info-container']//h3/a/text()").get() ,
					'Image': response.xpath(f"//div[@class='td-big-grid-wrapper']/div[2]/div[{div}]/div[@class='td-module-thumb']//a/img/@src").get()
				}
			length = len(response.xpath(f"//div[@class='td-ss-main-content']//div[@class='td-block-row']"))
			for o_div in range(1, length + 1):
				yield{
					'Image': response.xpath(f"//div[@class='td-ss-main-content']//div[@class='td-block-row'][{o_div}]//div[@class='td-block-span6'][1]//img/@src").get(),
					'h_link': response.xpath(f"//div[@class='td-ss-main-content']//div[@class='td-block-row'][{o_div}]//div[@class='td-block-span6'][1]//h3/a/@href").get(),
					'h_text':response.xpath(f"//div[@class='td-ss-main-content']//div[@class='td-block-row'][{o_div}]//div[@class='td-block-span6'][1]//h3/a/text()").get()
				}
				yield{
					'Image': response.xpath(f"//div[@class='td-ss-main-content']//div[@class='td-block-row'][{o_div}]//div[@class='td-block-span6'][2]//img/@src").get(),
					'h_link': response.xpath(f"//div[@class='td-ss-main-content']//div[@class='td-block-row'][{o_div}]//div[@class='td-block-span6'][2]//h3/a/@href").get(),
					'h_text':response.xpath(f"//div[@class='td-ss-main-content']//div[@class='td-block-row'][{o_div}]//div[@class='td-block-span6'][2]//h3/a/text()").get()
				}
		else:
			data = response.xpath(f"//div[@class='td-post-content tagdiv-type']/p/text() | //div[@class='td-post-content tagdiv-type']/h3//text() ").getall()
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

			pst_img = response.xpath("//div[@class='td-post-featured-image']//a//@href").get()

			yield{
				'Data': rec,
				'Post_image': pst_img
			}



# if __name__ == '__main__':
# 	process = CrawlerProcess()
# 	process.crawl(AnimeNewsNFacts,'https://animenewsandfacts.com/the-hidden-dungeon-episode-12/','details')
# 	process.start()


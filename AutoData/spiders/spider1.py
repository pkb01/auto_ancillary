import scrapy
#import re
from AutoData.items import AncillaryDetailsItem


class AncillaryDetailsSpider(scrapy.Spider):
	name = "AncillaryDetails"
	allowed_domains = ["fundoodata.com"]

	def urlFunc():
		url_list = []
		for i in range(151,218):
			url = "http://www.fundoodata.com/companies-in/automobile-auto-ancillaries-i223?&pageno="+str(i)+"&tot_rows=4357&total_results=4357&no_of_offices=0"
			url_list.append(url)
		return url_list

	start_urls = urlFunc()
 
	def parse(self, response):
		i=0
		f=0
		for sel in response.xpath("//*[@class='search-result-right']"):
			item = AncillaryDetailsItem()
			#item['companyName'] = sel.xpath("a/text()").extract()
			#item['industry'] = sel.xpath("//div[@class='normal-detail']//tr[1]/td[2]/text()").extract()
			if f == 3 :
				pass
			else:
				l2 = response.xpath("//*[@class='normal-detail']//tr[5]/td[2]/text()").extract()[i]
				if l2 is not None:
					item['city'] = l2.replace(" ","").replace("\n","").replace("\t","")[1:]
				else:
					item['city'] = "Not Found"
				l3 = response.xpath("//*[@class='normal-detail']//tr[3]/td[2]/text()").extract()[i]
				if l3 is not None:
					item['companyType'] = l3[2:]
				else:
					item['companyType'] = "Not Found"
				i+=1
			f+=1
			detail_url = sel.xpath("a/@href").extract_first()
			if detail_url is not None:
				item['MainPageUrl'] = "http://fundoodata.com/"+ detail_url
				request = scrapy.Request(item['MainPageUrl'], callback=self.parseAncillayDetails)
				request.meta['item'] = item
				yield request			

	def parseAncillayDetails(self, response):
		item = response.meta['item']	
		item = self.getPromoterDetials(item, response)		
		return item

	def getPromoterDetials(self, item, response):
		item['companyName'] = response.xpath("//*[@class='search-page-heading-red']/text()").extract()[0]
		item['contactNumber'] = response.xpath("//*[@class='detail-line']/text()").extract()[0] 
		l1=response.xpath("//*[@class='detail-line']/a/text()").extract_first()
		if l1 is not None:
			item['companyWebsite'] = l1
		else:
			item['companyWebsite'] = "Not Found"
		return item

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http.request import Request
from mn3spider.items import TopicItem

class Mn3Spider(BaseSpider):
    name = "mn3topic"
    allowed_domains = ["joker.si/mn3njalnik"]
    start_urls = ["http://www.joker.si/mn3njalnik/index.php?showforum=4"]

    def parse(self, response):
	f = open("results.txt","w")
	items = []
	hxs = HtmlXPathSelector(response)
	#check if last page
	next = hxs.select('//ul[@class="ipsList_inline forward left"]//li[@class="next"]//a/@href').extract()
	if len(next) > 0:
		yield Request(next[0],self.parse)
        topic_list = hxs.select('//div[@class="ipsBox"]//div[@class="ipsBox_container"]//table//tr')[1:]
        for topic in topic_list:
		item = TopicItem()	
		item['title'] = topic.select('td[@class="col_f_content "]//a[@class="topic_title"]/text()').extract()[0]
		item['author'] = topic.select('td[@class="col_f_content "]//a[@class="_hovertrigger url fn "]//text()').extract()[0]
		item['date'] = topic.select('td[@class="col_f_content "]//a[@class="topic_title"]//@title').extract()[0] #contains date, but also contains redundant data, TODO
		item['url'] = topic.select('td[@class="col_f_content "]//a[@class="topic_title"]//@href').extract()[0] #contains session info, which is irrelevant, TODO
		item['replies'] = topic.select('td[@class="col_f_views desc blend_links"]//a//text()').extract()[0] #string, TODO
		item['views'] = topic.select('td[@class="col_f_views desc blend_links"]//li[@class="views desc"]//text()').extract()[0] #string, TODO
		items.append(item)
		f.write(str(item)+"\n")
	f.close()
	return items

	

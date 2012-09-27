from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from mn3spider.items import TopicItem

class Mn3Spider(BaseSpider):
    name = "mn3spider"
    allowed_domains = ["joker.si/mn3njalnik"]
    start_urls = ["http://www.joker.si/mn3njalnik/index.php?showforum=14"]

    def parse(self, response):
	items = []
	hxs = HtmlXPathSelector(response)
        topic_list = hxs.select('//div[@class="ipsBox"]//div[@class="ipsBox_container"]//table//tr')[1:]
        for topic in topic_list:
		item = TopicItem()	
		item['title'] = topic.select('td[@class="col_f_content "]//a[@class="topic_title"]/text()').extract()[0]
		item['author'] = topic.select('td[@class="col_f_content "]//a[@class="topic_title"]/text()').extract()[0]
		item['date'] = topic.select('td[@class="col_f_content "]//a[@class="topic_title"]/text()').extract()[0] #contains date, but also contains redundant data, TODO
		item['url'] = topic.select('td[@class="col_f_content "]//a[@class="topic_title"]//@href').extract()[0] #contains session info, which is irrelevant, TODO
		item['replies'] = topic.select('td[@class="col_f_views desc blend_links"]//a//text()').extract()[0] #string, TODO
		item['views'] = topic.select('td[@class="col_f_views desc blend_links"]//li[@class="views desc"]//text()').extract()[0] #string, TODO
		items.append(item)
		print item
	return items

	
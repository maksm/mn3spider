from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http.request import Request
from mn3spider.items import TopicItem

#known possible issues:
# more than 1000 views or replies could not be counted
# when logged in, urls don't contain session variables anymore, so no processing is needed
class Mn3Topic(BaseSpider):
    name = "mn3topic"
    allowed_domains = ["joker.si"]
    start_urls = ["http://www.joker.si/mn3njalnik/index.php?showforum=4"]

    def parse(self, response):
        f = open("results.txt","w")
        items = []
        hxs = HtmlXPathSelector(response)
        #check if last page
        next = hxs.select('//ul[@class="ipsList_inline forward left"]//li[@class="next"]//a/@href').extract()
        if len(next) > 0:
            a = next[0].split('?')
            b = a[1].split('&')
            url = a[0]+"?"+b[1]+"&"+b[2]+"&"+b[3]+"&"+b[4]+"&"+b[5]+"&"+b[6]
            yield Request(url,self.parse)
    
        topic_list = hxs.select('//div[@class="ipsBox"]//div[@class="ipsBox_container"]//table//tr')[1:]
        for topic in topic_list:
            item = TopicItem()	
            item['title'] = topic.select('td[@class="col_f_content "]//a[@class="topic_title"]/text()').extract()[0]
            item['author'] = topic.select('td[@class="col_f_content "]//a[@class="_hovertrigger url fn "]//text()').extract()[0]
            date = topic.select('td[@class="col_f_content "]//a[@class="topic_title"]//@title').extract()[0]
            a = date.split()
            item['date']  = a[3]+" "+a[4]+" "+a[5]+" "+a[6]+" "+a[7]
            url = topic.select('td[@class="col_f_content "]//a[@class="topic_title"]//@href').extract()[0]
            a = url.split('?')
            b = a[1].split('&')
            item['url'] = a + "?" + b[1]
            a = b[1].split('')
            item['id'] = a[1]
            replies = topic.select('td[@class="col_f_views desc blend_links"]//a//text()').extract()[0]
            item['replies'] = replies.split()[0]
            item['views'] = topic.select('td[@class="col_f_views desc blend_links"]//li[@class="views desc"]//text()').extract()[0]
            #items.append(item)
            yield item
            f.write(str(item)+"\n")
        f.close()

	

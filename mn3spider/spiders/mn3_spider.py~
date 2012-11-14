from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http.request import Request
from mn3spider.items import TopicItem
from mn3spider.items import PostItem
from mn3spider.db import SqliteDB
import urlparse
#known possible issues:
# more than 1000 views or replies could not be counted
# when logged in, urls don't contain session variables anymore, so no processing is needed
db = SqliteDB()
#db.create()
class Mn3Topic(BaseSpider):
    name = "mn3topic"
    allowed_domains = ["joker.si"]
    start_urls = []
    forums = db.getForums()
    for forum in forums:
        url = "http://www.joker.si/mn3njalnik/index.php?showforum="+str(forum[0])
        start_urls.append(url)
    
    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        url = response.request.url
	forumid = urlparse.parse_qs(urlparse.urlparse(url).query)['showforum'][0]
	print forumid
	#raw_input("Press ENTER to continue")
        #check if last page
        next = hxs.select('//ul[@class="ipsList_inline forward left"]//li[@class="next"]//a/@href').extract()
        if len(next) > 0:
#            a = next[0].split('?')
#            b = a[1].split('&')
#            url = a[0]+"?"+b[1]+"&"+b[2]+"&"+b[3]+"&"+b[4]+"&"+b[5]+"&"+b[6]
             yield Request(next[0],self.parse)

        topic_list = hxs.select('//div[@class="ipsBox"]//div[@class="ipsBox_container"]//table//tr')[1:]
        for topic in topic_list:
            item = TopicItem()
	    
	    try:
		url = topic.select('td[@class="col_f_content "]//a[@class="topic_title"]//@href').extract()[0]
            	item['title'] = topic.select('td[@class="col_f_content "]//a[@class="topic_title"]/text()').extract()[0]
            	item['author'] = topic.select('td[@class="col_f_content "]//a[@class="_hovertrigger url fn "]//text()').extract()[0]
	    except Exception as e:
		if "Ni tem za prikaz." in topic.extract():
			pass
			continue
		if len(topic.select('td[@class="col_f_content "]//a[@class="_hovertrigger url fn "]//text()').extract()) < 0:
			item['author'] = "izbrisaniCHECK"
			pass
		else:
			print e
			print "--------------------------"
			topic.extract()
			print "--------------------------"
			print topic.select('td[@class="col_f_content "]//a[@class="topic_title"]/text()').extract()
			print topic.select('td[@class="col_f_content "]//a[@class="_hovertrigger url fn "]//text()').extract()
			print topic.select('td[@class="col_f_content "]//a[@class="topic_title"]//@href').extract()

            date = topic.select('td[@class="col_f_content "]//a[@class="topic_title"]//@title').extract()[0]
            a = date.split()
            item['date']  = date#a[3]+" "+a[4]+" "+a[5]+" "+a[6]+" "+a[7]
            url = topic.select('td[@class="col_f_content "]//a[@class="topic_title"]//@href').extract()[0]
#            a = url.split('?')
#            b = a[1].split('&')
#            url = a[0]+"?"
#            if len(b) > 1:
#                url = url+b[1]
#            else:
#                url = url+b[0]
#            item['url'] = url
            item['id'] = url.split('=')[-1]
            replies = topic.select('td[@class="col_f_views desc blend_links"]//a//text()').extract()[0]
            item['replies'] = replies.split()[0]
            item['views'] = topic.select('td[@class="col_f_views desc blend_links"]//li[@class="views desc"]//text()').extract()[0]
            db.insertTopic(forumid,  item['id'],  item['title'],  item['author'],  item['date'])
            #yield item


class Mn3Post(BaseSpider):
    name = "mn3post"
    allowed_domains = ["joker.si"]
    #start_urls should point to each topic in a subforum
    start_urls = []
    topics = db.getTopics()
    for topic in topics:
        url = "http://www.joker.si/mn3njalnik/index.php?showtopic="+str(topic[0])
        start_urls.append(url)
    print start_urls
        
    def parse(self, response):
        hxs = HtmlXPathSelector(response)
	url = response.request.url
	topicid = urlparse.parse_qs(urlparse.urlparse(url).query)['showtopic'][0]
        #check if last page
        next = hxs.select('//ul[@class="ipsList_inline forward left"]//li[@class="next"]//a/@href').extract()
        if len(next) > 0:
            a = next[0].split('?')
            b = a[1].split('&')
            if len(b)>2: url = a[0]+"?"+b[1]+"&"+b[2]
            else: url = next[0]
            yield Request(url,self.parse)
        
        posts = hxs.select('//div[@class="post_wrap"]')
        for post in posts:
            item = PostItem()
            item['num'] = post.select('h3[@class="row2"]/span/a[@rel="bookmark"]/text()').extract()[0][1:]
            postid= post.select('h3[@class="row2"]/span/a[@rel="bookmark"]/@href').extract()[0]
            postid = postid.split('&')
            item['id'] = postid[-1].split('=')[1]
            item['author'] = post.select('h3/span[@class="author vcard"]/a/text()').extract()[0]
            item['date'] = post.select('div[@class="post_body"]/p/abbr/text()').extract()[0]
            content = post.select('div[@class="post_body"]/div').extract()[0]
            item['content']  = content#[70:-10]
            db.insertPost(topicid,  item['id'] ,  item['num'],  item['author'],  item['date'],  item['content'])
            #yield item


# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class TopicItem(Item):
    # define the fields for your item here like:
    # name = Field()
	title = Field()
	#tags = Field()
	author = Field()
	date = Field()
	url = Field()
	replies = Field()
	views = Field()

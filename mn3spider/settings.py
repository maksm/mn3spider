# Scrapy settings for mn3spider project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'mn3spider'
BOT_VERSION = '0.2'

SPIDER_MODULES = ['mn3spider.spiders']
NEWSPIDER_MODULE = 'mn3spider.spiders'
#DEFAULT_ITEM_CLASS = 'mn3spider.items.MnSpiderItem'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)
DOWNLOAD_DELAY = 2
#ITEM_PIPELINES = ['isbullshit.pipelines.MongoDBPipeline',]
#
#MONGODB_SERVER = "localhost"
#MONGODB_PORT = 27017
#MONGODB_DB = "mn3"
#MONGODB_COLLECTION = "belatehnika"


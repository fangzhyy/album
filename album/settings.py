# Scrapy settings for album project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'album'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['album.spiders']
NEWSPIDER_MODULE = 'album.spiders'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)
ITEM_PIPELINES = {  
    'album.pipelines.AlbumPipeline':300  
}  

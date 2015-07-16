# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class AlbumItem(Item):
    # define the fields for your item here like:
    # name = Field()
    title = Field()
    image = Field()
    refer = Field()
    album_id = Field()
    people_id = Field()
    people_name = Field()
    relative = Field()
    album_name = Field()
    pass

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
import io
import sys
import json
import codecs 
class AlbumPipeline(object):
    f=codecs.open('albumUrls.json', 'wb','utf-8')
    def process_item(self, item, spider):
        jd=dict(item)
        s=json.dumps(jd, ensure_ascii=False)  + '\n'
        self.f.write(s)
        # with io.open('imageUrls.json', 'w', encoding='utf8') as json_file:
        #    json.dump(jd, json_file, ensure_ascii=False)   
        return item
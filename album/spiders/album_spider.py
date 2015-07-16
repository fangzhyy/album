# -*- coding: utf-8 -*-

from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy.http import Request
from album.items import AlbumItem
from album.pipelines import AlbumPipeline
import urllib2
import sys
import re
import time
import json
import codecs 

class AlbumSpider(BaseSpider):
    name = 'album'
    start_urls = []
    reload(sys)
    ids = [104245585]
    sys.setdefaultencoding('utf-8')    
    f=codecs.open('albumUrls.json', 'wb','utf-8')
    for id in ids:
        print id
        start_urls.append('http://www.douban.com/photos/album/%d'%id)
        
    def parse(self, response):
        hxs=Selector(response)
        sites=hxs.xpath('//span[@class="count"]/text()').extract();
        image_count=0
        for site in sites:
            id_str=""    
            for c in site:
                if(c>='0' and c<='9'):
                    id_str+=c
            if(len(id_str)>0):
                image_count=int(id_str)
                print 'count=',image_count
        base_url = response.url + '?start=%d'
        items = []
        album_id = re.search('\d+', response.url).group()
        
        for i in range(0, 18, 18):
            target_url=base_url%i
            print 'target_url=',target_url
            time.sleep(1)
            people_name = response.meta.get('people_name', None);
            people_id = response.meta.get('people_id', None);
            album_name = response.meta.get('album_name', None);
            yield Request(url=target_url,meta={"album_id" : album_id, 'people_id' : people_id,'people_name' : people_name, 'album_name' : album_name}
                          ,callback=self.parse_image_url)     
            
            #http://img3.douban.com/view/photo/large/public/p2250582305.jpg
    # http://www.douban.com/photos/photo/2250582305/

    #def parse_photo2main(self, response):
        ##从相对相册页面跳到主页面
        #sl = Selector(response)
        #sites = sl.xpath('//div[@class = "mod"]/h2/span[@class = "pl"]/a')
        #for site in sites:
            #main = site.xpath('./@href').extract()[0]
            #print 'main = ', main
            #yield Request(url = main, callback = self.parse_main)
    #def read_people_name(self, url):
        #info = str.split(url, '/')
        #offset = len(info) - 2
        #if(offset >= 0):
            #return info[offset]
        #return ''


    def parse_main(self, response):
        #get album sites frome album main page
        hxs = Selector(response)
        sites = hxs.xpath('//div[@class = "albumlst_r"]/div[@class = "pl2" ]/a')
        #get people name
        people_name = hxs.xpath('//div[@class = "info"]/h1/text()').extract()[0]
        #get people id
        people_id = re.search('\d+', response.url).group();
        
        for site in sites:
            album_name = site.xpath('./text()').extract()[0]
            site_url = site.xpath('./@href').extract()[0]
            print 'parse_main name = ', album_name, 'site_url = ', site_url
            yield Request(url = site_url, meta = {'people_name' : people_name, 'album_name': album_name, 'people_id' : people_id}, callback = self.parse)
        next_sites = hxs.xpath('//span[@class = "next"]/link[@rel = "next"]/@href').extract()
        for next_site in next_sites:
            yield Request(url = next_site, meta = {'people_name' : people_name,'people_id' : people_id}, callback = self.parse_main)
        
    def go_album_main(self, response):
        hxs = Selector(response)
        sites = hxs.xpath('//div[@class = "aside"]/div[@class="mod"]/h2/span[@class = "pl"]/a/@href').extract()
        for site in sites:
            print 'go_album_main site =', site
            yield Request(site, callback = self.parse_main)

    def parse_image_url(self, response):
        hxs=Selector(response)
        sites = hxs.xpath('//a[@class="photolst_photo"]')
        items = []
        album_id = response.meta['album_id']
        for site in sites:
            title = site.xpath('./@title').extract()[0].replace('\r\n', '_')
            print 'title=', title
            url = site.xpath('./@href').extract()[0]
            photo_id = re.search('\d+', url).group()         
            print 'photo_id=', photo_id
            item = AlbumItem()
            item['refer'] = url
            item['image'] = 'http://img3.douban.com/view/photo/large/public/p%s.jpg' % photo_id
            item['album_name'] = response.meta.get('album_name', None)
            item['title'] = title
            item['album_id'] = album_id
            item['people_id'] = response.meta.get('people_id', None)
            item['people_name'] = response.meta.get('people_name', None)
            if(len(title) > 0):
                info = title.split('_', 1)
                if(len(info) > 1):
                    relative = info[1].replace('_','')
                    item['relative'] = relative
                    if(relative.find('people') > 0):
                        album_url = relative + 'photos'
                        yield Request(url = album_url, callback = self.parse_main)
                    else:
                        yield Request(url = relative, callback = self.go_album_main)
            jd=dict(item)
            s=json.dumps(jd, ensure_ascii=False)  + '\n'
            self.f.write(s)            
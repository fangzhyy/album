# -*- coding: utf-8 -*-

from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy.http import Request
from album.items import AlbumItem
import urllib2
import sys
import re
import time


class AlbumSpider(BaseSpider):
    name = 'album'
    start_urls = []
    reload(sys)
    sys.setdefaultencoding('utf-8')    
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
        for i in range(0, image_count, 18):
            target_url=base_url%i
            print 'target_url=',target_url
            time.sleep(1)
            yield Request(url=target_url,meta={"album_id" : album_id},callback=self.parse_image_url)     
            
            #http://img3.douban.com/view/photo/large/public/p2250582305.jpg
    # http://www.douban.com/photos/photo/2250582305/

    def parse_photo2main(self, response):
        #从相对相册页面跳到主页面
        sl = Selector(response)
        sites = sl.xpath('//div[@class = "mod"]/h2/span[@class = "pl"]/a')
        for site in sites:
            main = site.xpath('./@href').extract()[0]
            print 'main = ', main
            yield Request(url = main, callback = self.parse_main)

    def parse_main(self, response):


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
            item['title'] = title
            item['album_id'] = album_id
            items.append(item)
        return items
            
            
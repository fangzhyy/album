# -*- coding: utf-8 -*-
import sys
import os
import time
import urllib2,httplib
import json
import codecs
import re

class albumDownload(object):
    filePath="../files"
    reload(sys)
    sys.setdefaultencoding('utf-8')    
    def startDownload(self):
        if not(os.path.exists(self.filePath)):
            os.mkdir(self.filePath)
        with codecs.open('../albumUrls.json', 'r','utf-8') as f:
            for line in f:
                self.doDownload(line)

    
    def doDownload(self, item):
        jitem = json.loads(item, encoding="utf-8")
        url=jitem['image'].encode('ascii')
        refer=jitem['refer']
        album_id = jitem['album_id']
        title = jitem['title']
        folder="../files/%s"%album_id
        if not(os.path.exists(folder)):
            os.mkdir(folder)        
        file_name = ''
        if(len(title) > 0):
            file_name = title.replace('/', '_')
        else:
            file_name = re.search('\d+', refer).group()
        if(os.path.exists(folder+"/%s.jpg"%file_name)):
            return False
        request=urllib2.Request(url)
        request.add_header("Referer", refer)
        request.add_header("User-Agent", "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; MyIE9; BTRS123646; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)")
        data=urllib2.urlopen(request).read()
        path = folder+"/%s.jpg"%file_name
        newFile=open(path,"w");
        newFile.write(data)
        newFile.close()
        return True
          
            
downloader=albumDownload()
downloader.startDownload()
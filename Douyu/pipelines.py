# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import os
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from Douyu.settings import IMAGES_STORE
import pymongo
 
class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )
    
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
    
    def process_item(self, item, spider):
        name = item.collection
        self.db[name].insert(dict(item))
        return item
    
    def close_spider(self, spider):
        self.client.close()


# 新的管线类，用于处理二进制文件
class DouyuPipeline(ImagesPipeline):
 	#def file_path(self, request, response=None, info=None):
        #url = request.url
        #file_name = url.split('/')[-1]
        #return file_name
    # 二进制下载，电影视频实际都可以，会自动调用download模组的函数
    def get_media_requests(self, item, info):
        image_link = item['imagelink']
        yield scrapy.Request(image_link)
     
    # 这个方法会在一次处理的最后调用（从返回item也可以推理出）
    # result表示下载的结果状态
    def item_completed(self, results, item, info):
        # print(results)
        # [(True, {'url': 'https://rpic.douyucdn.cn/acrpic/170827/3034164_v1319.jpg',
        # 'checksum': '7383ee5f8dfadebf16a7f123bce4dc45', 'path': 'full/6faebfb1ae66d563476449c69258f2e0aa24000a.jpg'})]
        image_path = [x['path'] for ok,x in results if ok]
        os.rename(IMAGES_STORE + '/'+ image_path[0], IMAGES_STORE+ '/' + item['nickname'] + '.jpg')
        if not image_path:
            raise scrapy.DropItem('Image Downloaded Failed')
        return item

import json
from Douyu.items import DouyuItem
import scrapy
from urllib.parse import urlencode



class DouyuspiderSpider(scrapy.Spider):
    name = "DouyuSpider"
    allowed_domains = ["douyucdn.cn"]
    baseURL = 'http://capi.douyucdn.cn/api/v1/getVerticalRoom?limit=20&offset='
    offset = 0
    start_urls = [baseURL + str(offset)]

    default_headers = {
        'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding' : 'gzip, deflate',
        'Accept-Language' : 'zh-CN,zh;q=0.9',
        'Cache-Control' : 'max-age=0',
        'Connection' : 'keep-alive',
        'Host' : 'capi.douyucdn.cn',
        'Upgrade-Insecure-Requests' : '1',
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    }
    def start_requests(self):
            for url in self.start_urls:
                yield scrapy.Request(url = url, headers = self.default_headers, callback = self.parse)


    def parse(self, response):
        # .load和磁盘交互，.loads处理字符串
        data_list = json.loads(response.body.decode('utf-8'))['data']
        if not len(data_list):
            return
 
        for data in data_list:
            item = DouyuItem()
            item['nickname'] = data['nickname']
            item['imagelink'] = data['vertical_src']
            item['online'] = data['online']
            item['game_name'] = data['game_name']
            item['anchor_city'] = data['anchor_city']
            yield item
 
        self.offset += 20
        yield scrapy.Request(self.baseURL + str(self.offset), callback=self.parse)
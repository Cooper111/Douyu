import scrapy
 
 
class DouyuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    collection = table = 'images'
    
    nickname = scrapy.Field()
    imagelink = scrapy.Field()
    online = scrapy.Field()
    game_name = scrapy.Field()
    anchor_city = scrapy.Field()
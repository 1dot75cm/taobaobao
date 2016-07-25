# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field

class TaobaoItem(Item):
    nid = Field()
    nick = Field()
    user_id = Field()
    item_loc = Field()
    shop_url = Field()

    title = Field()
    category = Field()
    categories = Field()
    pic_url = Field()
    detail_url = Field()
    reserve_price = Field()
    view_price = Field()
    view_sales = Field()
    comment_count = Field()
    comment_url = Field()

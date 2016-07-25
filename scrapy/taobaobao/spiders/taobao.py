# Get all product information for taobao.com

from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from taobaobao.items import TaobaoItem
import json

class TaobaoSpider(CrawlSpider):
    name = "taobao"
    allowed_domains = ["taobao.com"]
    start_urls = ["https://s.taobao.com/list?seller_type=taobao&json=on"]

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, self.parse_item, headers={
                "User-Agent": "Mozilla/5.0 (X11; Linux; rv:47.0) Gecko/20100101 Firefox/47.0"
            })

    def parse_item(self, response):
        d = json.loads(response.body.decode())
        if 'common' in d['mods']['nav']['data']:
            for i in d['mods']['nav']['data']['common'][0]['sub']:
                url = self.start_urls[0] + "&cat=%s" % i['value']
                yield Request(url, callback=self.parse_item)

        elif 'data' in d['mods']['pager']:
            pv = d['mods']['pager']['data']['currentPage'] * \
                 d['mods']['pager']['data']['pageSize']
            url = self.start_urls[0] + "&cat=%s&s=%s" % (
                d['mods']['nav']['data']['breadcrumbs']['catpath'][-1]['value'],
                pv)
            for i in d['mods']['itemlist']['data']['auctions']:
                item = TaobaoItem()
                item['nick'] = i['nick']
                item['user_id'] = i['user_id']
                item['item_loc'] = i['item_loc']
                item['shop_url'] = i['shopLink']

                item['nid'] = i['nid']
                item['title'] = i['title']
                item['category'] = i['category']
                item['categories'] = []
                item['pic_url'] = i['pic_url']
                item['detail_url'] = i['detail_url']
                item['reserve_price'] = i['reserve_price']
                item['view_price'] = i['view_price']
                item['view_sales'] = i['view_sales']
                item['comment_count'] = i['comment_count']
                item['comment_url'] = i['comment_url']
                for i in d['mods']['nav']['data']['breadcrumbs']['catpath']:
                    item['categories'].append({'name':i['name'], 'catid':i['catid']})
                yield item
            yield Request(url, callback=self.parse_item)

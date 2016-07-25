# -*- coding: utf-8 -*-
import pymongo
import json

def main():
    conn = pymongo.MongoClient('127.0.0.1', 27017)
    db = conn['taobao']
    goods_coll = db['goods']
    cate_coll = db['categories']

    print('Reading categories.')
    cate = set()
    for i in goods_coll.find():
        cate.add(json.dumps(i['categories']))

    for j in cate:
        obj = json.loads(j)
        catid = obj[-1]['catid']
        #cate_coll.insert(dict(categories=obj))
        cate_coll.update({'categories.catid': {'$regex': catid}},
                         dict(categories=obj), upsert=True)

    print('Categories:', len(cate))
    conn.close()

if __name__ in '__main__':
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pymongo
import json
import math
from bson.objectid import ObjectId

from config import mongodb

print('mongodb', mongodb)

myclient = pymongo.MongoClient(host=mongodb['host'], port=mongodb['port'], connect=False)
db = myclient[mongodb['name']]


class ObjectIdEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

# def connection(**kw):
#     global db
#     myclient = pymongo.MongoClient(kw.get('host', 'localhost'), kw.get('port', 27017))
#     db = myclient["python_blog"]

class Model(dict):
    def __init__(self, database=None):
        self.collection = db[database]

    def find(self):
        return self.collection.find()

    def find_all(self, **kw):
        currentPage = kw.get('currentPage', None)
        pageSize = kw.get('pageSize', None)
        orderBy = kw.get('orderBy', None)
        data = self.collection.find()
        total = data.count()
        if currentPage is not None and pageSize is not None:
            skip = (currentPage - 1) * pageSize
            data.skip(skip).limit(pageSize)

        result = dict(list=list(data),total=total, currentPage=currentPage, pageSize=pageSize, totalPage=math.ceil(total/pageSize))
        return json.loads(ObjectIdEncoder().encode(result))


    # def find_all_to_json(self, **kw):
    #     data = self.find_all(**kw)
    #     return json.loads(ObjectIdEncoder().encode(data))

    def find_one(self, id):
        return self.collection.find_one({'_id': ObjectId(id)})

    def find_one_by_where(self, where):
        user = self.collection.find_one(where)
        if user is None:
            return None
        return json.loads(ObjectIdEncoder().encode(user))

    def insert_one(self, data):
        self.collection.insert_one(data)

    def insert_many(self, data):
        self.collection.insert_many(data)

    def replace_one(self, data):
        current = self.find_one(data['_id'])
        self.collection.replace_one(current, data)

    def find_one_and_update(self, id, data):
        self.collection.find_one_and_update({'_id': ObjectId(id)}, {'$set': data})
        return JSONEncoder().encode({
            'data': None,
            'message': '删除成功zz',
            'code': 200
        })

    def find_one_and_delete(self, id):
        self.collection.find_one_and_delete({'_id': ObjectId(id)})
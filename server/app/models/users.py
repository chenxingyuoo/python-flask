#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# from . import db
from .orm import Model
from bson.objectid import ObjectId

class Users(Model):
    def __init__(self):
        super().__init__(database = 'users')
        # self.usersCol = db['users']

    # def save(self, data):
    #     self.usersCol.insert(data)
    #
    # def find(self, page = 1, page_size = 10):
    #     skip = (page - 1) * page_size
    #     return self.usersCol.find().skip(skip).limit(page_size)
    #
    # def find_all(self):
    #     return self.usersCol.find()
    #
    # def find_one(self, id):
    #     return self.usersCol.find_one({'_id' : ObjectId(id)})

# users = Users()

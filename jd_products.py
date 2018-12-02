#!/usr/bin/env python
# -*- coding:utf-8 -*-

from utils import *;
from config import *;
from pymongo import *;
import json;

class Jd_products:
    __db = '';

    @classmethod
    def get_db(cls):
        if not cls.__db :
            client = MongoClient(Config.mongodb.url);
            cls.__db = client.jdproduct;
        return  cls.__db;


    @classmethod
    def get_categories(cls):
        return Jd_products.get_db().JDCategory.find({});

    @classmethod
    def get_products_by_category(cls,cid):
        db = Jd_products.get_db();
        return db.JDProduct.find({'cid':cid});

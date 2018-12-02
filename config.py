#!/usr/bin/env python
# -*- coding: utf-8 -*-



class Mongodb:
    url = '';
    
    def __init__(self,url):
        self.url = url;

class Mysql:
    host = '';
    username = '';
    password = '';
    db = '';


    def __init__(self,host,username,password,db):
        self.host = host;
        self.username = username;
        self.password = password;
        self.db = db;


class Config:
     work_dir = '/';
     mongodb = Mongodb('mongodb://192.168.20.137');
     mysql = Mysql('192.168.11.118','hishop.oc','himall123','hishop_oc_test_mall');

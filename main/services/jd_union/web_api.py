#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
    :Author: yuangezhizao
    :Time: 2019/2/13 0013 21:55
    :Site: https://www.yuangezhizao.cn
    :Copyright: © 2019 yuangezhizao <root@yuangezhizao.cn>
"""
import json

import pymongo
import requests
from bson import ObjectId
from flask import current_app


def get_cookies():
    admin_cookie = pymongo.MongoClient(current_app.config['MONGODB_SETTINGS']['host'])['jd']['admin_cookie']
    return admin_cookie.find_one({'_id': ObjectId('5c5d7e772c56c16ebefbeff7')})['cookie']


def create_url(id, pid, url):
    web_api_url = 'https://union.jd.com/api/receivecode/getCode'
    headers = {
        'Content-type': 'application/json',
        'Cookie': get_cookies(),
    }
    data = {"data": {"materialType": 7, "promotionId": pid, "promotionType": 3, "promotionTypeId": id,
                     "receiveType": "cps", "wareUrl": url, "isSmartGraphics": 0}}
    r = requests.post(web_api_url, data=json.dumps(data), headers=headers).text
    return r

#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
    :Author: yuangezhizao
    :Time: 2019/5/26 0026 14:31
    :Site: https://www.yuangezhizao.cn
    :Copyright: © 2019 yuangezhizao <root@yuangezhizao.cn>
"""
from main.plugins.extensions import db


class Coupon_Limit(db.Document):
    meta = {
        'collection': 'coupon_limit'
    }
    sku = db.IntField(required=True)
    update_time = db.DateTimeField()
    endTime = db.DateTimeField()
    couponid = db.StringField()
    batchid = db.StringField()

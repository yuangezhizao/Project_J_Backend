#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
    :Author: yuangezhizao
    :Time: 2019/1/28 0028 13:20
    :Site: http://www.yuangezhizao.cn
    :Copyright: © 2019 yuangezhizao <root@yuangezhizao.cn>
"""
from main.plugins.extensions import db


class Coupon_Orig(db.Document):
    meta = {
        'collection': 'projectj_coupons'
    }
    key = db.StringField(required=True, primary_key=True)  # 主键即为 _id，优惠券 key
    roleid = db.StringField()
    limitStr = db.StringField()
    quota = db.StringField()
    discount = db.StringField()
    discountpercent = db.FloatField()
    batchId = db.StringField()
    batchCount = db.IntField()
    beginTime = db.DateTimeField()
    endTime = db.DateTimeField()
    update_time = db.DateTimeField()
    url = db.StringField()
    salesurl = db.StringField()
    batchurl = db.StringField()
    from_url = db.StringField()

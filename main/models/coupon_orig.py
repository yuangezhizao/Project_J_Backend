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
    limitStr = db.StringField()  # 仅可购买
    quota = db.StringField()  # 满
    discount = db.StringField()  # 减
    discountpercent = db.FloatField()  # 折扣幅度
    batchId = db.StringField()
    batchCount = db.IntField()  # 限量
    beginTime = db.DateTimeField()  # 开始时间
    endTime = db.DateTimeField()  # 结束时间
    update_time = db.DateTimeField()
    url = db.StringField()  # 优惠券地址
    salesurl = db.StringField()  # 活动地址
    batchurl = db.StringField()  # 可用地址
    from_url = db.StringField()  # 来源地址

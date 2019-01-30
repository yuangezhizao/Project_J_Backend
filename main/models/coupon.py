#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
    :Author: yuangezhizao
    :Time: 2019/1/28 0028 13:20
    :Site: http://www.yuangezhizao.cn
    :Copyright: © 2019 yuangezhizao <root@yuangezhizao.cn>
"""
from main.plugins.extensions import db


class Coupon(db.Document):
    meta = {
        'collection': 'projectj_coupons'
    }
    key = db.StringField(required=True, primary_key=True)  # 主键即为 _id，优惠券 key
    name = db.StringField(required=True)  # 优惠券名称
    strength = db.StringField(required=True)  # 优惠力度
    act_url = db.StringField(required=True)  # 活动地址
    url = db.StringField(required=True)  # 优惠券地址
    beginTime = db.DateTimeField(required=True)  # 开始时间
    endTime = db.DateTimeField(required=True)  # 结束时间

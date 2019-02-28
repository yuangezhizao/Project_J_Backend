#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
    :Author: yuangezhizao
    :Time: 2019/1/28 0028 23:13
    :Site: http://www.yuangezhizao.cn
    :Copyright: © 2019 yuangezhizao <root@yuangezhizao.cn>
"""
from main.plugins.extensions import db


class Good(db.Document):
    meta = {
        'collection': 'projectj_goods'
    }
    sku = db.IntField(required=True, primary_key=True)  # 主键即为 _id，商品 id
    update_time = db.DateTimeField(required=True)  # 更新时间
    price_now = db.FloatField(required=True)  # 当前价格
    img = db.StringField(required=True)  # 图片地址
    title = db.StringField(required=True)  # 商品名称
    url = db.StringField(required=True)  # 商品地址
    discountpercent = db.FloatField(required=True)  # 降价幅度
    jd_price = db.FloatField(required=True)  # 京东价格
    buy_count = db.IntField(required=True)  # 购买数量
    his_price = db.FloatField(required=True)

    cuxiao = db.StringField()  # 促销
    coupon_discount = db.IntField()
    coupon_quota = db.IntField()
    coupon_roleid = db.StringField()
    coupon_url = db.StringField()
    coupon_key = db.StringField()

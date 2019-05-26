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
    price_now = db.FloatField(required=True)  # 【用完各种优惠之后的价格】
    img = db.StringField(required=True)  # 图片地址
    title = db.StringField(required=True)  # 商品名称
    url = db.StringField(required=True)  # 商品地址
    discountpercent = db.FloatField(required=True)  # 降价幅度【打折比例（后端处理保留两位小数）】
    jd_price = db.FloatField(required=True)  # 京东价格
    buy_count = db.IntField(required=True)  # 【购买 x 件 可享最大优惠】
    his_price = db.FloatField(required=True)  # 【历史最低价】

    cuxiao = db.StringField()  # 【促销方案 直接返回】
    coupon_discount = db.IntField()  # 【优惠券减多少钱】
    coupon_quota = db.IntField()  # 【优惠券满多少元可用】
    coupon_roleid = db.StringField()
    coupon_url = db.StringField()  # 【优惠券链接 存在这个字段时 要有领取优惠券】
    coupon_key = db.StringField()

    bigsort = db.StringField()

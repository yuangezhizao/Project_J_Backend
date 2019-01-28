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
    sku = db.StringField(required=True, primary_key=True)  # 主键即为 _id，商品 id
    title = db.StringField(required=True)  # 商品名称
    prize = db.StringField(required=True)  # 商品价格

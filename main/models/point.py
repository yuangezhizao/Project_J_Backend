#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
    :Author: yuangezhizao
    :Time: 2019/1/29 0029 00:59
    :Site: http://www.yuangezhizao.cn
    :Copyright: © 2019 yuangezhizao <root@yuangezhizao.cn>
"""
import datetime

from main.plugins.extensions import db


class WX_Point(db.Document):
    meta = {
        'collection': 'projectj_wx_points'
    }
    uid = db.IntField(required=True)  # 用户 uid
    value = db.StringField(required=True)  # 已解锁值
    insert_time = db.DateTimeField(default=datetime.datetime.utcnow())

#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
    :Author: yuangezhizao
    :Time: 2019/1/28 0028 15:20
    :Site: http://www.yuangezhizao.cn
    :Copyright: © 2019 yuangezhizao <root@yuangezhizao.cn>
"""
import datetime

from main.plugins.extensions import db


class Feedback(db.Document):
    meta = {
        'collection': 'projectj_wx_feedback'
    }
    uid = db.IntField(required=True)  # 用户 uid
    msg = db.StringField(required=True)  # 意见反馈内容
    insert_time = db.DateTimeField(default=datetime.datetime.now())

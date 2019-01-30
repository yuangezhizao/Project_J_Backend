#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
    :Author: yuangezhizao
    :Time: 2019/1/30 0030 16:15
    :Site: http://www.yuangezhizao.cn
    :Copyright: © 2019 yuangezhizao <root@yuangezhizao.cn>
"""
import datetime

from main.plugins.extensions import db


class WX_Invite(db.Document):
    meta = {
        'collection': 'projectj_wx_invites'
    }
    uid = db.IntField(required=True)  # 用户 uid
    from_uid = db.IntField(required=True)  # 上家 uid
    type = db.StringField(required=True)  # 类型
    value = db.StringField(required=True)  # 值
    insert_time = db.DateTimeField(default=datetime.datetime.utcnow())

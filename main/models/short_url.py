#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
    :Author: yuangezhizao
    :Time: 2019/3/6 0006 15:05
    :Site: https://www.yuangezhizao.cn
    :Copyright: © 2019 yuangezhizao <root@yuangezhizao.cn>
"""
from main.plugins.extensions import db


class Short_URL(db.Document):
    meta = {
        'collection': 'projectj_short_url'
    }
    id = db.StringField(required=True, primary_key=True)
    jid = db.StringField(required=True)
    url = db.StringField(required=True)
    update_time = db.DateTimeField(required=True)

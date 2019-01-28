#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
    :Author: yuangezhizao
    :Time: 2019/1/28 0028 15:34
    :Site: http://www.yuangezhizao.cn
    :Copyright: © 2019 yuangezhizao <root@yuangezhizao.cn>
"""
import datetime

from main.plugins.extensions import db


class WX_Info(db.Document):
    meta = {
        'collection': 'projectj_wx_info'
    }
    title = db.StringField(required=True)  # 标题
    content = db.StringField(required=True)  # 内容
    insert_time = db.DateTimeField(default=datetime.datetime.now())

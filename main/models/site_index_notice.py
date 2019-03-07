#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
    :Author: yuangezhizao
    :Time: 2019/3/7 0007 16:16
    :Site: https://www.yuangezhizao.cn
    :Copyright: © 2019 yuangezhizao <root@yuangezhizao.cn>
"""
import datetime

from main.plugins.extensions import db


class Site_Index_Notice(db.Document):
    meta = {
        'collection': 'site_index_notice'
    }
    title = db.StringField(required=True)  # 标题
    content = db.StringField(required=True)  # 内容
    insert_time = db.DateTimeField(default=datetime.datetime.utcnow())

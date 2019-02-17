#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
    :Author: yuangezhizao
    :Time: 2019/2/17 0017 19:11
    :Site: https://www.yuangezhizao.cn
    :Copyright: © 2019 yuangezhizao <root@yuangezhizao.cn>
"""
from main.plugins.extensions import db


class Socialmedia_Loc(db.Document):
    meta = {
        'collection': 'jdunion_socialmedia_loc'
    }
    id = db.IntField(required=True, primary_key=True)  # 主键即为 _id，推广位 ID
    promotionName = db.StringField(required=True)  # 推广位名称
    pid = db.StringField(required=True)  # PID
    mediaId = db.IntField(required=True)  # 社交媒体 ID
    createTime = db.DateTimeField(required=True)  # 创建时间

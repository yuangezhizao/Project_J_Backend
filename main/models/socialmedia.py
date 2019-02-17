#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
    :Author: yuangezhizao
    :Time: 2019/2/17 0017 16:56
    :Site: https://www.yuangezhizao.cn
    :Copyright: © 2019 yuangezhizao <root@yuangezhizao.cn>
"""
from main.plugins.extensions import db


class Socialmedia(db.Document):
    meta = {
        'collection': 'jdunion_socialmedia'
    }
    id = db.IntField(required=True, primary_key=True)  # 主键即为 _id，社交媒体 ID
    unionId = db.IntField(required=True)  # 联盟 ID（无用）
    mediaName = db.StringField(required=True)  # 社交媒体名称
    homeUrl = db.StringField(required=True)  # 用户主页地址
    loginAccount = db.StringField(required=True)  # 登录账号
    createTime = db.DateTimeField(required=True)  # 创建时间
    updateTime = db.DateTimeField(required=True)  # 更新时间

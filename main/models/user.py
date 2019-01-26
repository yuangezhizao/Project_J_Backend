#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
    :Author: yuangezhizao
    :Time: 2019/1/24 0024 19:45
    :Site: http://www.yuangezhizao.cn
    :Copyright: © 2019 yuangezhizao <root@yuangezhizao.cn>
"""
import datetime

from main.plugins.extensions import db


class WX_Users(db.Document):
    meta = {
        "collection": "wx_users"
    }
    uid = db.IntField()  # 自增 uid
    openid = db.StringField(required=True)  # 用户唯一标识（前端传入 wxcode，后端去微信服务器调用 code2Session 获得）
    # unionid  # 用户在开放平台的唯一标识符，在满足 UnionID 下发条件的情况下会返回，详见 UnionID 机制说明。（前端传入 wxcode，后端去微信服务器调用 code2Session 获得）
    session_key = db.StringField(required=True)  # 会话密钥（前端传入 wxcode，后端去微信服务器调用 code2Session 获得）

    userinfo = db.StringField(required=True)  # 用户信息对象，不包含 openid 等敏感信息（前端传入）

    token = db.StringField(required=True)  # 开发者服务器自定义登录态
    member_since = db.DateTimeField(default=datetime.datetime.utcnow)  # 用户注册时间
    last_seen = db.DateTimeField(default=datetime.datetime.utcnow)  # 用户上次活跃

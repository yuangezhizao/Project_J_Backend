#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
    :Author: yuangezhizao
    :Time: 2019/1/24 0024 19:45
    :Site: http://www.yuangezhizao.cn
    :Copyright: © 2019 yuangezhizao <root@yuangezhizao.cn>
"""
import datetime

import requests
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from main.apis.v0_1.outputs import unauthorized, success, forbidden
from main.plugins.extensions import db


class WX_User(db.Document):
    meta = {
        'collection': 'projectj_wx_users'
    }
    uid = db.IntField(required=True, unique=True)  # 自增 uid
    openid = db.StringField(unique=True)  # 用户唯一标识（前端传入 wxcode，后端去微信服务器调用 code2Session 获得）
    # unionid  # 用户在开放平台的唯一标识符，在满足 UnionID 下发条件的情况下会返回，详见 UnionID 机制说明。（前端传入 wxcode，后端去微信服务器调用 code2Session 获得）
    session_key = db.StringField(default=None)  # 会话密钥（前端传入 wxcode，后端去微信服务器调用 code2Session 获得）

    userinfo = db.DictField(default=None)  # 用户信息对象，不包含 openid 等敏感信息（前端传入）

    token = db.StringField(default=None)  # 开发者服务器自定义登录态
    member_since = db.DateTimeField(default=datetime.datetime.utcnow)  # 用户登录时间（填写完邀请码之后才算注册）
    # last_seen = db.DateTimeField(default=datetime.datetime.utcnow)  # 用户上次活跃，考虑到后期的负载还是禁用吧

    # phonenumber = db.StringField(default=None)  # 用户绑定的手机号（国外手机号会有区号）
    # purePhoneNumber = db.StringField(default=None)  # 没有区号的手机号
    # countryCode = db.StringField(default=None)  # 区号
    # 微信官方获取手机号接口，暂不使用

    # invitation_code = db.StringField(default=None)
    # 邀请码供他人使用，详细说明见初始化
    invitees = db.IntField(default=None)
    # 被邀请人，别人的 uid
    points = db.IntField(default=0)

    # 此处积分为零，详细说明见下方

    def code2Session(self, wxcode):
        url = 'https://api.weixin.qq.com/sns/jscode2session?appid={0}&secret={1}&js_code={2}&grant_type=authorization_code'.format(
            current_app.config['APPID'], current_app.config['APPSECRET'], wxcode)
        r = requests.get(url).json()
        if not r['errcode']:
            openid = r['openid']
            session_key = r['session_key']
            # unionid = r['unionid']
            return [openid, session_key]
        else:
            return forbidden(r['errmsg'])

    '''
    def init_invitation_code(self):
        from itsdangerous import URLSafeSerializer
        s = URLSafeSerializer(current_app.config['SECRET_KEY'])
        self.invitation_code = s.dumps(self.uid)
        # 邀请码为 URL安全序列化（SECRET_KEY 参与计算）的结果，因此上次提交注销之前的 SECRET_KEY
    # 邀请码使用用户 uid，故不使用此法（invitation_code 还太长……
    '''

    def generate_token(self):
        expiration = 3600
        # 令牌过期时间暂定为一小时
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        token = s.dumps({'uid': self.uid})
        self.token = token.decode('ascii')
        self.save()
        return {'token': self.token, 'expires_in': expiration}

    '''
    from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature
    def set_invitees(self, invitation_code):
        if self.invitees:
            return forbidden('你已填过邀请码')
        s = URLSafeSerializer(current_app.config['SECRET_KEY'])
        try:
            invitees = s.loads(invitation_code)
        except BadSignature:
            return unauthorized('邀请码无效')
        self.invitees = invitees
        self.points = 1000
        self.save()
        return success('1000 积分已到账')
    '''

    def set_invitees(self, uid):
        if self.invitees:
            return forbidden('你已填过邀请码')
        query = WX_User.objects(uid=uid)
        if not query:
            return unauthorized('邀请码无效')
        self.invitees = uid
        self.points = 1000
        self.save()
        return success('1000 积分已到账')

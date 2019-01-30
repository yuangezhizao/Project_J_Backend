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

from main.apis.v0_1.outputs import forbidden
from main.models.invite import WX_Invite
from main.models.unlock import WX_Unlock
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
    member_since = db.DateTimeField(default=datetime.datetime.utcnow())  # 用户登录时间（填写完邀请码之后才算注册）
    last_seen = db.DateTimeField(default=datetime.datetime.utcnow())  # 用户刷新 token 时间

    # phonenumber = db.StringField(default=None)  # 用户绑定的手机号（国外手机号会有区号）
    # purePhoneNumber = db.StringField(default=None)  # 没有区号的手机号
    # countryCode = db.StringField(default=None)  # 区号
    # 微信官方获取手机号接口，暂不使用

    # invitation_code = db.StringField(default=None)
    # 邀请码供他人使用，详细说明见初始化
    inviter = db.IntField(default=None)
    # 邀请人，上家的 uid
    points = db.IntField(default=1000)

    # 初始化积分为 1000

    def code2Session(self, wxcode):
        url = 'https://api.weixin.qq.com/sns/jscode2session?appid={0}&secret={1}&js_code={2}&grant_type=authorization_code'.format(
            current_app.config['APPID'], current_app.config['APPSECRET'], wxcode)
        r = requests.get(url).json()
        if not 'errmsg' in r:
            openid = r['openid']
            session_key = r['session_key']
            # unionid = r['unionid']
            # 此处确认暂时没有返回 unionid
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
        try:
            s.loads(self.token)
            return {'token': self.token}
            # 令牌未过期，使用旧令牌
        except Exception as e:
            pass
            # 令牌已过期，生成新令牌
        token = s.dumps({'uid': self.uid})
        self.token = token.decode('ascii')
        self.save()
        self.ping()
        return {'token': self.token, 'expires_in': expiration}

    def ping(self):
        now_time = datetime.datetime.utcnow()
        self.last_seen = now_time
        self.save()

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

    def invite_check(self, from_uid):
        check = WX_Invite.objects(uid=self.uid, from_uid=from_uid).first()
        if not check:
            return ''
        else:
            return check.insert_time.strftime('%Y-%m-%d %H:%M:%S')

    def invite_action(self, from_uid, type, value):
        if not self.inviter:
            # 此处也可如下判断
            # action = WX_Invite.objects(uid=self.uid, from_uid=from_uid).first()
            # 未邀请，入库
            if from_uid == self.uid:
                return forbidden('你不能自己邀请自己')
            query = WX_User.objects(uid=from_uid)
            # 此处与解锁动作不同，需验证 from_uid 真实性
            if query:
                user = query.first()
                points = user.points
                points += 100
                # 暂定邀请成功给与邀请人 100 积分
                query.update_one(set__points=points, )
            else:
                return forbidden('邀请人异常')
            invite = WX_Invite()
            invite.uid = self.uid
            invite.from_uid = from_uid
            invite.type = type
            invite.value = value
            invite.save()
            # 关联表保存
            self.inviter = from_uid
            self.save()
            # 用户表保存
            insert_time = invite.insert_time.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return forbidden('已填写过邀请人')
        return [self.uid, insert_time]

    def unlock_check(self, value):
        check = WX_Unlock.objects(uid=self.uid, value=value).first()
        if not check:
            return ''
        else:
            return check.insert_time.strftime('%Y-%m-%d %H:%M:%S')

    def unlock_action(self, value):
        action = WX_Unlock.objects(uid=self.uid, value=value).first()
        if not action:
            # 未解锁，扣减积分
            if self.points > 0:
                # 积分大于零，走扣减流程
                unlock = WX_Unlock()
                unlock.uid = self.uid
                unlock.value = value
                unlock.save()
                # 关联表保存
                self.points = self.points - 1
                self.save()
                # 用户表保存
                insert_time = unlock.insert_time.strftime('%Y-%m-%d %H:%M:%S')
            else:
                # 积分小于零，无法兑换
                return forbidden('用户积分不足')
        else:
            insert_time = action.insert_time.strftime('%Y-%m-%d %H:%M:%S')
        return [self.uid, insert_time]

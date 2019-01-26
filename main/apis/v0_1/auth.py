#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
    :Author: yuangezhizao
    :Time: 2019/1/24 0024 19:39
    :Site: http://www.yuangezhizao.cn
    :Copyright: © 2019 yuangezhizao <root@yuangezhizao.cn>
"""
from functools import wraps

from flask import g, current_app, request
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired

from main.apis.v0_1.outputs import unauthorized
from main.models.user import WX_Users


def generate_token(user):
    expiration = 3600
    # 令牌过期时间暂定为一小时
    s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
    token = s.dumps({'uid': user.uid}).decode('ascii')
    return token, expiration


def validate_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except SignatureExpired:
        return unauthorized('SignatureExpired')  # valid token, but expired
    except BadSignature:
        return unauthorized('BadSignature')  # invalid token
    # 以下来自 def _get_openid_token(token):
    query = WX_Users.objects(uid=data['uid'])[0]
    g.current_user = query  # 用户信息放到 g 中以便使用
    return True


def get_token():
    # Flask/Werkzeug do not recognize any authentication types
    # other than Basic or Digest, so here we parse the header by hand.
    # if 'Authorization' in request.headers:
    #     try:
    #         token_type, token = request.headers['Authorization'].split(None, 1)
    #     except ValueError:
    #         # The Authorization header is either empty or has no token
    #         token_type = token = None
    # else:
    #     token_type = token = None
    #
    # return token_type, token
    # TODO：小程序不支持 cookies 操作，但 token 暂未放在 headers 中，
    return request.form.get('token', None)


def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_token()

        # Flask normally handles OPTIONS requests on its own, but in the
        # case it is configured to forward those to the application, we
        # need to ignore authentication headers and let the request through
        # to avoid unwanted interactions with CORS.
        if request.method != 'OPTIONS':
            if token is None:
                return unauthorized('token_missing')
            if not validate_token(token):
                # 在 validate_token 中输出详细信息，故走不到下一行
                return unauthorized('invalid_token')
        return f(*args, **kwargs)

    return decorated

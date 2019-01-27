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

from main.apis.v0_1 import api_v0_1
from main.apis.v0_1.outputs import unauthorized, success, bad_request
from main.models.user import WX_User


def validate_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except SignatureExpired:
        return 'SignatureExpired'  # valid token, but expired
    except BadSignature:
        return 'BadSignature'  # invalid token
    # 以下来自 def _get_openid_token(token):
    query = WX_User.objects(uid=data['uid'])[0]
    g.user = query  # 用户信息放到 g 中以便使用
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
    return request.args.get('token', None)


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
            result = validate_token(token)
            if result != True:
                # 切记此处不可改成 if not result
                return unauthorized(result)
        return f(*args, **kwargs)

    return decorated


@api_v0_1.route('/user/login', methods=['GET', 'POST'])
def user_login():
    try:
        wxcode = request.form.get('wxcode')
        userinfo = request.form.get('userinfo')
        signature = request.form.get('signature')
        encryptedData = request.form.get('encryptedData')
        iv = request.form.get('iv')
        print('wxcode：' + wxcode)
        print('userinfo：' + userinfo)
        print('signature：' + signature)
        print('encryptedData：' + encryptedData)
        print('iv：' + iv)
        # TODO：开放数据校验与解密（防止伪造）
    except Exception as e:
        print(e)
        return bad_request('参数错误')

    user = WX_User()

    data = user.code2Session(wxcode)
    if isinstance(data, list):
        openid, session_key = data
    else:
        return data
    query = WX_User.objects(openid=openid)
    # 已注册用户处理：在此之前不要保存用户
    if query:
        query.update_one(set__session_key=session_key,
                         # set__unionid=unionid,
                         set__userinfo=userinfo
                         )
    else:
        user.uid = WX_User.objects.all().count() + 1 + current_app.config['FAKE_NUM']
        user.openid = openid
        user.session_key = session_key
        # user.unionid = unionid
        user.userinfo = userinfo
        user.save()
        # user.init_invitation_code()
    token = user.generate_token()
    return success(token)


@api_v0_1.route('/user/set_invitees', methods=['GET', 'POST'])
@auth_required
def user_set_invitees():
    try:
        invitation_code = request.form.get('invitation_code')
    except Exception as e:
        print(e)
        return bad_request('参数错误')
    r = g.user.set_invitees(invitation_code)
    return r


@api_v0_1.route('/user/invitation_code')
@auth_required
def user_invitation_code():
    return success(g.user.uid)


@api_v0_1.route('/user/points')
@auth_required
def user_points():
    return success(g.user.points)

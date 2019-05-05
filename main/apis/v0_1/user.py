#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
    :Author: yuangezhizao
    :Co-authored-by: liyanzhe
    :Time: 2019/1/24 0024 19:39
    :Site: http://www.yuangezhizao.cn
    :Copyright: © 2019 liyanzhe <liyanzhe@igengmei.com>
    :Copyright: © 2019 yuangezhizao <root@yuangezhizao.cn>
"""
import json
from functools import wraps

import requests
from flask import current_app, request
from flask import g
from flask import redirect
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired

from main.apis.v0_1 import api_v0_1
from main.apis.v0_1.outputs import bad_request
from main.apis.v0_1.outputs import unauthorized, success
from main.models.feedback import WX_Feedback
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
    query = WX_User.objects(uid=data['uid']).first()
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


def save_invite(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        from_uid = request.get_json()['from_uid'] if (
                (request.get_json() is not None) and ('from_uid' in request.get_json())) else None
        if from_uid:
            if not g.user.inviter:
                key = request.args.get('key', None)
                lotteryCode = request.args.get('lotteryCode', None)
                if key:
                    g.user.invite_action(g.user.uid, from_uid, 1, key)
                elif lotteryCode:
                    g.user.invite_action(g.user.uid, from_uid, 2, lotteryCode)
                else:
                    pass
        else:
            pass
        return f(*args, **kwargs)

    return decorated


@api_v0_1.route('/user/login', methods=['GET', 'POST'])
def user_login():
    data = request.get_json()
    try:
        wxcode = data['wxcode']
        userinfo = data['userinfo']
        signature = data['signature']
        encryptedData = data['encryptedData']
        iv = data['iv']
        from_uid = data['formUID'] if (('formUID' in data) and isinstance(data['formUID'], int)) else -1
        print('wxcode：' + wxcode)
        print('userinfo：' + userinfo)
        print('signature：' + signature)
        print('encryptedData：' + encryptedData)
        print('iv：' + iv)
        print('formUID：' + str(from_uid))
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
                         set__userinfo=eval(userinfo)
                         )
        user = query.first()
    else:
        user.uid = WX_User.objects.all().count() + 1 + current_app.config['FAKE_NUM']
        user.openid = openid
        user.session_key = session_key
        # user.unionid = unionid
        user.userinfo = eval(userinfo)
        user.save()
        user.invite_action(from_uid, 1, None)
        # user.init_invitation_code()
    token = user.generate_token()
    return success(token)


@api_v0_1.route('/user/inviter', methods=['GET', 'POST'])
@auth_required
def user_inviter():
    try:
        from_uid = request.get_json()['from_uid']
    except Exception as e:
        print(e)
        return bad_request('参数错误')
    invite_result = g.user.invite_action(from_uid, None, None)
    if isinstance(invite_result, list):
        uid, insert_time = invite_result
    else:
        return invite_result
    r = {
        'invite_Time': insert_time
    }
    return success(r)


@api_v0_1.route('/user/userinfo')
@auth_required
def user_userinfo():
    user = g.user
    userinfo = user.userinfo
    r = {
        'uid': user.uid,
        'nickname': userinfo['nickName'],
        'gender': userinfo['gender'],
        'avatarurl': userinfo['avatarUrl'],
        'member_since': user['member_since'].strftime('%Y-%m-%d %H:%M:%S'),
        'points': user['points'],
        # 'token': userinfo.token
        # token 仅在登录接口处返回一次
    }
    return success(r)


@api_v0_1.route('/user/feedback', methods=['GET', 'POST'])
@auth_required
def user_feedback():
    try:
        msg = request.get_json()['msg']
    except Exception as e:
        print(e)
        return bad_request('参数错误')
    feedback = WX_Feedback()
    feedback.uid = g.user.uid
    feedback.msg = msg
    feedback.save()
    return success('提交成功')


@api_v0_1.route('/user/pc/login')
def user_pc_login():
    try:
        code = request.args.get('code')
    except Exception as e:
        print(e)
        return bad_request('参数错误')
    access_params = {
        'appid': current_app.config['WX_OPEN_APP_ID'],
        'secret': current_app.config['WX_OPEN_APP_SECRET'],
        'code': code,
        'grant_type': 'authorization_code'
    }
    access_res = requests.get('https://api.weixin.qq.com/sns/oauth2/access_token', params=access_params).json()
    print(access_res)
    if 'errcode' in access_res:
        return bad_request(data=access_res)
    access_token = access_res['access_token']
    openid = access_res['openid']
    user_info_params = {
        'access_token': access_token,
        'openid': openid
    }
    userinfo = requests.get('https://api.weixin.qq.com/sns/userinfo', params=user_info_params)
    userinfo = json.loads(str(userinfo.content, encoding='utf-8'))
    print(userinfo)
    if 'errcode' in userinfo:
        return bad_request(data=userinfo)
    query = WX_User.objects(openid=openid)
    if query:
        query.update_one(set__access_token=access_token,
                         set__userinfo=userinfo)
        user = query.first()
    else:
        user = WX_User()
        user.uid = WX_User.objects.all().count() + 1 + current_app.config['FAKE_NUM']
        user.openid = openid
        user.unionid = userinfo['unionid']
        user.access_token = access_token
        user.userinfo = userinfo
        user.save()
    token = user.generate_token(3600 * 24 * 7)
    userinfo.pop('openid')
    userinfo.pop('unionid')
    userinfo['uid'] = user.uid
    # return success({'userinfo': userinfo, 'token': token})

    res = redirect(current_app.config['URL'])
    res.set_cookie('token', str(token['token']), max_age=7 * 24 * 3600)
    res.set_cookie('headimgurl', str(userinfo['headimgurl']), max_age=7 * 24 * 3600)
    res.set_cookie('nickname', str(userinfo['nickname']), max_age=7 * 24 * 3600)
    return res


@api_v0_1.route('/user/status')
def user_status():
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
    return success(0)


@api_v0_1.route('/user/pc/userinfo')
@auth_required
def user_pc_userinfo():
    user = g.user
    userinfo = user.userinfo
    r = {
        'nickname': userinfo['nickname'],
        'headimgurl': userinfo['headimgurl'],
    }
    return success(r)

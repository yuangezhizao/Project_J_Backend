#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
    :Author: yuangezhizao
    :Time: 2019/5/4 0004 11:07
    :Site: https://www.yuangezhizao.cn
    :Copyright: © 2019 yuangezhizao <root@yuangezhizao.cn>
"""

import json

import requests
from flask import current_app, request

from main.apis.v0_1.outputs import success, bad_request
from main.models.user import WX_User
from . import pc_bp


@pc_bp.route('/user/login', methods=['POST'])
def user_login():
    try:
        code = request.form['code']
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
    token = user.generate_token(7200)
    userinfo.pop('openid')
    userinfo.pop('unionid')
    userinfo['uid'] = user.uid
    return success({'userinfo': userinfo, 'token': token})

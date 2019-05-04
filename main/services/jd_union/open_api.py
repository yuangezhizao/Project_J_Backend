#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
    :Co-authored-by: liyanzhe
    :Author: yuangezhizao
    :Time: 2019/4/30 0030 12:06
    :Site: https://www.yuangezhizao.cn
    :Copyright: © 2019 liyanzhe <liyanzhe@igengmei.com>
    :Copyright: © 2019 yuangezhizao <root@yuangezhizao.cn>
"""
import datetime
import hashlib
import json

import requests
from flask import current_app


def create_url(common_url):
    params = {
        'method': 'jd.union.open.promotion.common.get',
        'app_key': current_app.config['JD_UNION_APP_KEY'],
        'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'format': 'json',
        'v': '1.0',
        'sign_method': 'md5',
        'param_json': {
            'promotionCodeReq': {'siteId': current_app.config['JD_UNION_SITE_ID'], 'materialId': common_url}
        },
    }
    param_list = ['app_key', 'format', 'method', 'param_json', 'sign_method', 'timestamp', 'v']
    request_url = 'https://router.jd.com/api?'
    secret_str = current_app.config['JD_UNION_APP_SECRET']
    for item in param_list:
        if item == 'param_json':
            params[item] = str(params.get(item)).replace(' ', '')
        secret_str += str(item) + str(params.get(item))
        request_url += '{name}={value}&'.format(name=item, value=params.get(item))
    secret_str += current_app.config['JD_UNION_APP_SECRET']
    sign = hashlib.md5(secret_str.encode('utf-8')).hexdigest()
    request_url += 'sign=' + str(sign).upper()
    res = requests.get(request_url)
    data = json.loads(str(res.content, encoding='utf-8'))
    if 'errorResponse' in data:
        print(data)
        return [False, data['errorResponse']]
    data = json.loads(data['jd_union_open_promotion_common_get_response']['result'])
    if data['code'] == 200:
        return [True, data['data']['clickURL']]
    else:
        print(data)
        return [False, data]

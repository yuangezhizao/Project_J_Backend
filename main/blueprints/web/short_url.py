#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
    :Author: yuangezhizao
    :Time: 2019/3/6 0006 14:51
    :Site: https://www.yuangezhizao.cn
    :Copyright: © 2019 yuangezhizao <root@yuangezhizao.cn>
"""
from flask import request, redirect

from main.apis.v0_1.outputs import bad_request, not_found
from main.models.short_url import Short_URL
from . import web_bp


@web_bp.route('/short_url')
def short_url_index():
    try:
        id = request.args.get('id')
    except Exception as e:
        print(e)
        return bad_request('参数错误')
    short_url = Short_URL.objects(id=id).first()
    if short_url is None:
        return not_found('键无效')
    return redirect(short_url.url)

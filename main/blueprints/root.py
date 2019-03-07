#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
    :Author: yuangezhizao
    :Time: 2019/1/25 0025 21:50
    :Site: http://www.yuangezhizao.cn
    :Copyright: © 2019 yuangezhizao <root@yuangezhizao.cn>
"""
from flask import Blueprint, request, redirect

from main.apis.v0_1.outputs import bad_request, not_found
from main.models.short_url import Short_URL

root_bp = Blueprint('root', __name__)


@root_bp.route('/')
def hello_world():
    try:
        id = request.args.get('id')
    except Exception as e:
        print(e)
        return bad_request('参数错误')
    short_url = Short_URL.objects(id=id).first()
    if short_url is None:
        return not_found('键无效')
    return redirect(short_url.url)

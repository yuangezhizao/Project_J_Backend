#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
    :Author: yuangezhizao
    :Time: 2019/1/25 0025 21:50
    :Site: http://www.yuangezhizao.cn
    :Copyright: © 2019 yuangezhizao <root@yuangezhizao.cn>
"""
from flask import Blueprint, make_response

root_bp = Blueprint('root', __name__)


@root_bp.route('/')
def hello_world():
    return 'Hello, Flask!'


@root_bp.route('/jd_root.txt')
def jd_verify():
    return 'e95d2f4a675fe6f2b231093ef0892219c03e13e310499f23'


@root_bp.route('/robots.txt')
def robots():
    response = make_response('''User-agent: *
Disallow: /admin/''')
    response.headers['Content-Type'] = 'text/plain; charset=utf-8'
    return response

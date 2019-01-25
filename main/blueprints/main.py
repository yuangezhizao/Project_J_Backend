#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
    :Author: yuangezhizao
    :Time: 2019/1/25 0025 21:50
    :Site: http://www.yuangezhizao.cn
    :Copyright: © 2019 yuangezhizao <root@yuangezhizao.cn>
"""
from flask import Blueprint

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def hello_world():
    return 'Hello, Flask!'


@main_bp.route('/jd_root.txt')
def jd_verify():
    return 'e95d2f4a675fe6f2b231093ef0892219c03e13e310499f23'

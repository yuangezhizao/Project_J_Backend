#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
    :Author: yuangezhizao
    :Time: 2019/1/25 0025 21:50
    :Site: http://www.yuangezhizao.cn
    :Copyright: © 2019 yuangezhizao <root@yuangezhizao.cn>
"""
from flask import Blueprint, render_template

root_bp = Blueprint('root', __name__)


@root_bp.route('/')
def hello_world():
    return render_template('index.html')

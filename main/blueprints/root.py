#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
    :Author: yuangezhizao
    :Time: 2019/1/25 0025 21:50
    :Site: http://www.yuangezhizao.cn
    :Copyright: © 2019 yuangezhizao <root@yuangezhizao.cn>
"""
from flask import Blueprint, render_template, redirect

from main.apis.v0_1.outputs import not_found
from main.models.short_url import Short_URL

root_bp = Blueprint('root', __name__)


@root_bp.route('/')
def hello_world():
    return render_template('index.html')


@root_bp.route('/s/<id>')
def short_url(id):
    s = Short_URL.objescts(id=id).first()
    if short_url is None:
        return not_found('键无效')
    return redirect(s.url)

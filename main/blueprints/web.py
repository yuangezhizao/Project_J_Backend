#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
    :Author: yuangezhizao
    :Time: 2019/2/13 0013 22:33
    :Site: https://www.yuangezhizao.cn
    :Copyright: © 2019 yuangezhizao <root@yuangezhizao.cn>
"""
from flask import Blueprint, request

web_bp = Blueprint('web', __name__)


@web_bp.route('/jd_union/create_url')
def jd_union_create_url():
    from main.services.jd_union.web_api import create_url
    id = request.args.get('id')
    pid = request.args.get('pid')
    url = request.args.get('url')
    try:
        return create_url(id, pid, url)
    except Exception as e:
        return str(e)

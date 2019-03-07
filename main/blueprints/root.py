#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
    :Author: yuangezhizao
    :Time: 2019/1/25 0025 21:50
    :Site: http://www.yuangezhizao.cn
    :Copyright: © 2019 yuangezhizao <root@yuangezhizao.cn>
"""
from flask import Blueprint

from main.models.site_index_notice import Site_Index_Notice

root_bp = Blueprint('root', __name__)


@root_bp.route('/')
def hello_world():
    notice = Site_Index_Notice.objects.first()
    return '<html><body><h1>{0}</h1><h2>{1}</h2></body></html>'.format(notice['title'], notice['content'])

#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
    :Author: yuangezhizao
    :Time: 2019/2/15 0015 11:37
    :Site: https://www.yuangezhizao.cn
    :Copyright: © 2019 yuangezhizao <root@yuangezhizao.cn>
"""
from flask import Blueprint
from flask_cors import CORS

web_bp = Blueprint('web', __name__)

CORS(web_bp)

from . import jd_union, wx_feedback, wx_user, lottery, good, coupon, short_url

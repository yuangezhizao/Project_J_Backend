#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
    :Author: yuangezhizao
    :Time: 2019/1/24 0024 19:32
    :Site: http://www.yuangezhizao.cn
    :Copyright: © 2019 yuangezhizao <root@yuangezhizao.cn>
"""
from flask import Blueprint
from flask_cors import CORS

api_v0_1 = Blueprint('api_v0_1', __name__)

CORS(api_v0_1)

from . import outputs, user, coupon, info
# https://blog.csdn.net/hjxzb/article/details/78910832

#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
    :Author: yuangezhizao
    :Time: 2019/2/15 0015 11:37
    :Site: https://www.yuangezhizao.cn
    :Copyright: © 2019 yuangezhizao <root@yuangezhizao.cn>
"""
from flask import Blueprint

web_bp = Blueprint('web', __name__)

from main.blueprints.web import jd_union
from main.blueprints.web import wx_feedback
from main.blueprints.web import wx_user
from main.blueprints.web import lottery
from main.blueprints.web import goods

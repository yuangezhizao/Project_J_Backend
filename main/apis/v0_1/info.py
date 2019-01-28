#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
    :Author: yuangezhizao
    :Time: 2019/1/28 0028 15:13
    :Site: http://www.yuangezhizao.cn
    :Copyright: © 2019 yuangezhizao <root@yuangezhizao.cn>
"""
from main.apis.v0_1 import api_v0_1
from main.apis.v0_1.outputs import success
from main.models.info import WX_Info


@api_v0_1.route('/info/points')
def info_points():
    infos = WX_Info.objects.all()
    r = []
    for info in infos:
        new_info = {}
        new_info['title'] = info['title']
        new_info['content'] = info['content']
        r.append(new_info)
    return success(r)

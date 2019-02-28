#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
    :Author: yuangezhizao
    :Time: 2019/2/28 0028 19:35
    :Site: https://www.yuangezhizao.cn
    :Copyright: © 2019 yuangezhizao <root@yuangezhizao.cn>
"""
from flask import request

from main.apis.v0_1.outputs import success
from main.models.good import Good
from . import web_bp


@web_bp.route('/good', methods=['GET', 'POST'])
def good_index():
    page = request.get_json()['page'] if ((request.get_json() is not None) and ('page' in request.get_json())) else 1
    paginated_goods = Good.objects.order_by('update_time').paginate(page=page, per_page=10)
    r = []
    for good in paginated_goods.items:
        new_good = {}
        new_good['sku'] = good['sku']
        new_good['title'] = good['title']
        new_good['price_now'] = good['price_now']
        new_good['update_time'] = good['update_time'].strftime('%Y-%m-%d %H:%M:%S')
        new_good['url'] = good['url']
        r.append(new_good)
    next = page + 1 if paginated_goods.has_next else page
    r = {'goods': r, 'next': next, 'pages': paginated_goods.pages, 'has_next': paginated_goods.has_next}
    return success(r)

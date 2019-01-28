#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
    :Author: yuangezhizao
    :Time: 2019/1/28 0028 20:06
    :Site: http://www.yuangezhizao.cn
    :Copyright: © 2019 yuangezhizao <root@yuangezhizao.cn>
"""
from flask import request

from main.apis.v0_1 import api_v0_1
from main.apis.v0_1.outputs import success
from main.apis.v0_1.user import auth_required
from main.models.lottery import Lottery


@api_v0_1.route('/lottery', methods=['GET', 'POST'])
@auth_required
def lottery_index():
    page = request.get_json()['page'] if ((request.get_json() is not None) and ('page' in request.get_json())) else 1
    paginated_lotteries = Lottery.objects.paginate(page=page, per_page=10)
    r = []
    for lottery in paginated_lotteries.items:
        new_lottery = {}
        new_lottery['lotteryName'] = lottery['lotteryName']
        new_lottery['endTime'] = lottery['endTime'].strftime('%Y-%m-%d %H:%M:%S')
        r.append(new_lottery)
    next = page + 1 if paginated_lotteries.has_next else page
    r = {'coupons': r, 'next': next, 'pages': paginated_lotteries.pages, 'has_next': paginated_lotteries.has_next}
    return success(r)
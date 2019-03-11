#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
    :Author: yuangezhizao
    :Time: 2019/2/17 0017 20:00
    :Site: https://www.yuangezhizao.cn
    :Copyright: © 2019 yuangezhizao <root@yuangezhizao.cn>
"""
import datetime

from flask import request

from main.apis.v0_1.outputs import success, bad_request
from main.models.lottery import Lottery
from . import web_bp


@web_bp.route('/lottery')
def lottery_index():
    page = int(request.args.get('page')) if (
            (request.args.get('page') is not None) and (request.args.get('page') != '')) else 1
    # TODO：wtforms
    has_expired = request.args.get('has_expired', 0)
    sort = request.args.get('sort', 0)
    if int(sort) == 1:
        sort = '-endTime'
    else:
        sort = 'endTime'
    if int(has_expired) == 1:
        paginated_lotteries = Lottery.objects().order_by(sort).paginate(page=page, per_page=100)
    else:
        now_time = datetime.datetime.now()
        paginated_lotteries = Lottery.objects(endTime__gt=now_time).order_by(sort).paginate(page=page, per_page=100)
    r = []
    for lottery in paginated_lotteries.items:
        new_lottery = {}
        new_lottery['lotteryCode'] = lottery['lotteryCode']
        new_lottery['lotteryName'] = lottery['lotteryName']
        new_lottery['beginTime'] = lottery['beginTime'].strftime('%Y-%m-%d %H:%M:%S')
        new_lottery['endTime'] = lottery['endTime'].strftime('%Y-%m-%d %H:%M:%S')
        new_lottery['url'] = lottery['url']
        r.append(new_lottery)
    next = page + 1 if paginated_lotteries.has_next else page
    r = {'lotteries': r, 'next': next, 'pages': paginated_lotteries.pages, 'has_next': paginated_lotteries.has_next}
    return success(r)


@web_bp.route('/lottery/search', methods=['GET', 'POST'])
def lottery_search():
    # TODO：等学会 ES 的
    try:
        content = request.form['content']
    except Exception as e:
        print(e)
        return bad_request('参数错误')
    r = {
        'content': content,
    }
    return success(r)

#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
    :Author: yuangezhizao
    :Time: 2019/1/28 0028 20:06
    :Site: http://www.yuangezhizao.cn
    :Copyright: © 2019 yuangezhizao <root@yuangezhizao.cn>
"""
import datetime
import hashlib

import math
from flask import request, g, url_for, current_app

from main.apis.v0_1 import api_v0_1
from main.apis.v0_1.outputs import success, bad_request, not_found
from main.apis.v0_1.user import auth_required
from main.models.lottery import Lottery
from main.models.short_url import Short_URL
from main.plugins.extensions import es
from main.services.jd_union.open_api import create_url


@api_v0_1.route('/lottery', methods=['GET', 'POST'])
@auth_required
def lottery_index():
    page = request.get_json()['page'] if ((request.get_json() is not None) and ('page' in request.get_json())) else 1
    now_time = datetime.datetime.now()
    paginated_lotteries = Lottery.objects(endTime__gt=now_time).order_by('endTime').paginate(page=page, per_page=10)
    r = []
    for lottery in paginated_lotteries.items:
        new_lottery = {}
        new_lottery['lotteryCode'] = lottery['lotteryCode']
        new_lottery['lotteryName'] = lottery['lotteryName']
        new_lottery['endTime'] = lottery['endTime'].strftime('%Y-%m-%d %H:%M:%S')
        r.append(new_lottery)
    next = page + 1 if paginated_lotteries.has_next else page
    r = {'lotteries': r, 'next': next, 'pages': paginated_lotteries.pages, 'has_next': paginated_lotteries.has_next}
    return success(r)


@api_v0_1.route('/lottery/detail', methods=['GET', 'POST'])
@auth_required
def lottery_detail():
    try:
        lotteryCode = request.get_json()['lotteryCode']
    except Exception as e:
        print(e)
        return bad_request('参数错误')
    lottery = Lottery.objects(lotteryCode=lotteryCode).first()
    if lottery is None:
        return not_found('抽奖码无效')
    new_lotteryPrize = []
    for prize in lottery.lotteryPrize:
        new_prize = {}
        new_prize['prizeName'] = prize['prizeName']
        new_prize['prizeDesc'] = prize['prizeDesc']
        new_prize['sortOrder'] = prize['sortOrder']
        new_lotteryPrize.append(new_prize)
    status = -1 if (g.user.points == 0) else 1  # 默认需要解锁，返回 1，积分不足返回 -1
    check_result = g.user.unlock_check(lotteryCode)
    if check_result != '':
        status = 0  # 已经解锁
    r = {
        'lotteryCode': lottery.lotteryCode,
        'lotteryName': lottery.lotteryName,
        'beginTime': lottery.beginTime.strftime('%Y-%m-%d %H:%M:%S'),
        'endTime': lottery.endTime.strftime('%Y-%m-%d %H:%M:%S'),
        'lotteryPrize': new_lotteryPrize,
        # 'url': lottery.url
        # url 为解锁字段
        'sellingpoints': 1,
        'points': g.user.points,
        'status': status,
        'unlock_Time': check_result,
    }
    return success(r)


@api_v0_1.route('/lottery/unlock', methods=['GET', 'POST'])
@auth_required
def lottery_unlock():
    try:
        lotteryCode = request.get_json()['lotteryCode']
    except Exception as e:
        print(e)
        return bad_request('参数错误')
    lottery = Lottery.objects(lotteryCode=lotteryCode).first()
    if lottery is None:
        return not_found('抽奖码无效')
    new_lotteryPrize = []
    for prize in lottery.lotteryPrize:
        new_prize = {}
        new_prize['prizeName'] = prize['prizeName']
        new_prize['prizeDesc'] = prize['prizeDesc']
        new_prize['sortOrder'] = prize['sortOrder']
        new_lotteryPrize.append(new_prize)
    status = -1 if (g.user.points == 0) else 1  # 默认需要解锁，返回 1，积分不足返回 -1
    check_result = g.user.unlock_check(lotteryCode)
    if check_result != '':
        status = 0  # 已经解锁
    else:
        result = g.user.unlock_action(lotteryCode)
        if isinstance(result, list):
            uid, check_result = result
            status = 0  # 解锁成功
        else:
            return result
    r = {
        'url': lottery.url,
        'points': g.user.points,
        'status': status,
        'unlock_Time': check_result,
    }
    return success(r)


@api_v0_1.route('/lottery/search')
def lottery_search():
    count = int(request.args.get('count', 15)) if (int(request.args.get('count', 15)) in [8, 15]) else 15
    page = int(request.args.get('page', 1)) if (int(request.args.get('page', 1)) < 100) else 100
    content = request.args.get('content', '')
    query = {
        'size': count,
        'from': (page - 1) * count
    }
    if content:
        query['query'] = {
            'multi_match': {
                'query': content,
                'fields': ['lotteryName']
            }
        }
    query['sort'] = [{'endTime': 'desc'}]
    result = es.search(index='jd', doc_type='lottery_detail', body=query)
    data = []
    for lottery in result['hits']['hits']:
        new_lottery = {}
        new_lottery['lotteryCode'] = lottery['_id']
        new_lottery['lotteryName'] = lottery['_source'].get('lotteryName')
        new_lottery['beginTime'] = lottery['_source'].get('beginTime')  # .strftime('%Y-%m-%d %H:%M:%S')
        new_lottery['endTime'] = lottery['_source'].get('endTime')  # .strftime('%Y-%m-%d %H:%M:%S')
        data.append(new_lottery)
    pages = math.ceil(result['hits']['total'] / count)
    next = page + 1 if page < pages else page
    has_next = True if page < pages else False
    r = {'lotteries': data, 'next': next, 'pages': pages, 'has_next': has_next}
    return success(r)


@api_v0_1.route('/lottery/pc/unlock', methods=['GET', 'POST'])
@auth_required
def lottery_pc_unlock():
    try:
        lotteryCode = request.form['lotteryCode']
    except Exception as e:
        print(e)
        return bad_request('参数错误')
    lottery = Lottery.objects(lotteryCode=lotteryCode).first()
    if lottery is None:
        return not_found('抽奖码无效')
    url = lottery.url
    s = Short_URL.objects(url=url).first()
    if s:
        return success(url_for('root.short_url', jid=s.jid, _external=True))
    else:
        data = create_url(url)
        if data[0]:
            s = Short_URL()
            sign_hash = hashlib.md5()
            sign_hash.update((current_app.config['SALT'] + url).encode('utf-8'))
            s.jid = sign_hash.hexdigest()
            s.url = url
            s.create_url = data[1]
            s.update_time = datetime.datetime.utcnow()
            s.save()
            return success(url_for('root.short_url', jid=s.jid, _external=True))
        else:
            return bad_request(data[1])

#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
    :Author: yuangezhizao
    :Time: 2019/1/28 0028 13:34
    :Site: http://www.yuangezhizao.cn
    :Copyright: © 2019 yuangezhizao <root@yuangezhizao.cn>
"""
import math
from flask import request, g

from main.apis.v0_1 import api_v0_1
from main.apis.v0_1.outputs import success, bad_request, not_found
from main.apis.v0_1.user import auth_required
from main.models.coupon import Coupon
from main.plugins.extensions import es


@api_v0_1.route('/coupon', methods=['GET', 'POST'])
@auth_required
def coupon_index():
    page = request.get_json()['page'] if ((request.get_json() is not None) and ('page' in request.get_json())) else 1
    paginated_coupons = Coupon.objects.order_by('-update_time').paginate(page=page, per_page=10)
    r = []
    for coupon in paginated_coupons.items:
        new_coupon = {}
        new_coupon['key'] = coupon['key']
        new_coupon['limitStr'] = coupon['limitStr']
        new_coupon['coupon_name'] = '满 {0} 减 {1}'.format(coupon['quota'], coupon['discount'])
        r.append(new_coupon)
    next = page + 1 if paginated_coupons.has_next else page
    r = {'coupons': r, 'next': next, 'pages': paginated_coupons.pages, 'has_next': paginated_coupons.has_next}
    return success(r)


@api_v0_1.route('/coupon/detail', methods=['GET', 'POST'])
@auth_required
def coupon_detail():
    try:
        key = request.get_json()['key']
    except Exception as e:
        print(e)
        return bad_request('参数错误')
    coupon = Coupon.objects(key=key).first()
    if coupon is None:
        return not_found('优惠券码无效')
    status = -1 if (g.user.points == 0) else 1  # 默认需要解锁，返回 1，积分不足返回 -1
    check_result = g.user.unlock_check(coupon.key)
    if check_result != '':
        status = 0  # 已经解锁
    r = {
        'key': coupon.key,
        'limitStr': coupon.limitStr,
        'coupon_name': '满 {0} 减 {1}'.format(coupon['quota'], coupon['discount']),
        'discountpercent': coupon.discountpercent,
        'batchCount': coupon.batchCount,
        'beginTime': coupon.beginTime.strftime('%Y-%m-%d %H:%M:%S'),
        'endTime': coupon.endTime.strftime('%Y-%m-%d %H:%M:%S'),
        # 'url': coupon.url
        # 注释为解锁字段
        'sellingpoints': 1,
        'points': g.user.points,
        'status': status,
        'unlock_Time': check_result,
    }
    return success(r)


@api_v0_1.route('/coupon/unlock', methods=['GET', 'POST'])
@auth_required
def coupon_unlock():
    try:
        key = request.get_json()['key']
    except Exception as e:
        print(e)
        return bad_request('参数错误')
    coupon = Coupon.objects(key=key).first()
    if coupon is None:
        return not_found('优惠券码无效')
    status = -1 if (g.user.points == 0) else 1  # 默认需要解锁，返回 1，积分不足返回 -1
    check_result = g.user.unlock_check(coupon.key)
    if check_result != '':
        status = 0  # 已经解锁
    else:
        result = g.user.unlock_action(coupon.key)
        if isinstance(result, list):
            uid, check_result = result
            status = 0  # 解锁成功
        else:
            return result
    r = {
        'url': coupon.url,
        'salesurl': coupon.salesurl,
        'batchurl': coupon.batchurl,
        'from_url': coupon.from_url,
        'points': g.user.points,
        'status': status,
        'unlock_Time': check_result,
    }
    return success(r)


@api_v0_1.route('/coupon/search')
def coupon_search():
    Update_time, Disperent, Quota = 1, 2, 3
    # 枚举类型 按照什么排序规则排序
    count_allowed = [8, 28]
    page = int(request.args.get('page', 1))
    page = page if page < 100 else 100
    content = request.args.get('content', '')
    s_type = int(request.args.get('type', 1))
    count = int(request.args.get('count', 28))
    if count not in count_allowed:
        count = 28
    query = {
        'query': {
            'multi_match': {
                'query': content,
                'fields': ['limitStr', 'from_title', 'note', 'venderName']
            }
        },
        'size': count,
        'from': (page - 1) * count
    }
    if not content:
        query = {
            'size': count,
            'from': (page - 1) * count
        }
    if Update_time == s_type:
        sort = [{'update_time': 'desc'}]
    elif Disperent == s_type:
        sort = [{'discountpercent': 'asc'}]
    elif Quota == s_type:
        sort = [{'quota.keyword': 'desc'}]
    else:
        sort = [{'update_time': 'desc'}]
    query['sort'] = sort
    r = es.search(index='jd', doc_type='coupon_detail', body=query)
    data = []
    for item in list(r['hits']['hits']):
        if item['_source'].get('venderName'):
            data.append({
                '_id': item.get('_id'),
                # 'sort': item.get('sort'),
                # '_type': item.get('_type'),
                # '_source': {
                'venderName': item['_source'].get('venderName'),  # 店名
                # 'url': item['_source'].get('url'),
                # 'update_time': item['_source'].get('update_time'),
                # 'notes': item['_source'].get('notes'),
                'batchCount': item['_source'].get('batchCount'),
                # 'batchurl': item['_source'].get('batchurl'),
                # 'from_url': item['_source'].get('from_url'),
                'quota': item['_source'].get('quota'),
                # 'salesurl': item['_source'].get('salesurl'),
                # 'shopId': item['_source'].get('shopId'),
                'discount': item['_source'].get('discount'),
                'discountpercent': item['_source'].get('discountpercent'),  # x折
                'limitStr': item['_source'].get('limitStr'),
                # 'key': item['_source'].get('key')
                # } if item.get('_source') else {}
            })
    pages = math.ceil(r['hits']['total'] / count)
    next = page + 1 if page < pages else page
    has_next = True if page < pages else False
    r = {'result': data, 'next': next, 'pages': pages, 'has_next': has_next}
    return success(r)


@api_v0_1.route('/coupon/receive', methods=['GET', 'POST'])
def coupon_receive():
    try:
        key = request.form['key']
    except Exception as e:
        print(e)
        return bad_request('参数错误')
    query = {
        'query': {
            'multi_match': {
                'query': key,
                'fields': ['_id']
            }
        }
    }
    r = es.search(index='jd', doc_type='coupon_detail', body=query)
    if not len(r['hits']['hits']):
        return not_found('优惠券码无效')
    item = r['hits']['hits'][0]
    result = {
        'url': item['_source'].get('url'),
        'salesurl': item['_source'].get('salesurl'),
        'batchurl': item['_source'].get('batchurl'),
        'from_url': item['_source'].get('from_url'),
    }
    return success(result)

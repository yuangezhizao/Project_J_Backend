#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
    :Author: yuangezhizao
    :Time: 2019/1/28 0028 13:34
    :Site: http://www.yuangezhizao.cn
    :Copyright: © 2019 yuangezhizao <root@yuangezhizao.cn>
"""

import datetime
import hashlib

import math
from flask import current_app, request
from flask import g
from flask import url_for

from main.apis.v0_1 import api_v0_1
from main.apis.v0_1.outputs import bad_request
from main.apis.v0_1.outputs import not_found
from main.apis.v0_1.outputs import success
from main.apis.v0_1.user import auth_required
from main.models.coupon import Coupon
from main.models.short_url import Short_URL
from main.plugins.extensions import es
from main.services.jd_union.open_api import create_url


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
    count = int(request.args.get('count', 28)) if (int(request.args.get('count', 28)) in [5, 8, 28]) else 28
    page = int(request.args.get('page', 1)) if (int(request.args.get('page', 1)) < 100) else 100
    content = request.args.get('content', '')
    type = int(request.args.get('type', 1))
    query = {
        'size': count,
        'from': (page - 1) * count
    }
    if content:
        query['query'] = {
            'bool': {
                'must': {
                    'multi_match': {
                        'query': content,
                        'fields': ['limitStr', 'from_title', 'note', 'venderName']
                    }
                },
                'filter': {
                    'bool': {
                        'must': {
                            'range': {
                                'endTime': {
                                    'gte': 'now'
                                }
                            }
                        },
                        'filter': {
                            'exists': {
                                'field': 'limitStr'
                            }
                        },
                    }
                }
            }
        }
    else:
        query['query'] = {
            'bool': {
                'filter': {
                    'bool': {
                        'must': {
                            'range': {
                                'endTime': {
                                    'gte': 'now'
                                }
                            }
                        },
                        'filter': {
                            'exists': {
                                'field': 'limitStr'
                            }
                        }
                    }
                }
            }
        }
    if type == 2:
        query['sort'] = [{'discountpercent': 'asc'}]
    elif type == 3:
        query['sort'] = [{'quota.keyword': 'desc'}]
    else:
        query['sort'] = [{'update_time': 'desc'}]
    result = es.search(index='jd', doc_type='coupon_detail', body=query)
    data = []
    for coupon in result['hits']['hits']:
        new_coupon = {}
        new_coupon['key'] = coupon['_source'].get('key')
        new_coupon['limitStr'] = coupon['_source'].get('limitStr')
        new_coupon['coupon_name'] = '满 {0} 减 {1}'.format(coupon['_source'].get('quota'),
                                                         coupon['_source'].get('discount'))
        new_coupon['venderName'] = coupon['_source'].get('venderName')
        new_coupon['batchCount'] = coupon['_source'].get('batchCount')
        new_coupon['discountpercent'] = coupon['_source'].get('discountpercent')
        # new_coupon['_id'] = coupon.get('_id')
        # new_coupon['sort'] = coupon.get('sort')
        # new_coupon['_type'] = coupon.get('_type')
        # new_coupon['url'] = coupon['_source'].get('url')
        # new_coupon['update_time'] = coupon['_source'].get('update_time')
        # new_coupon['notes'] = coupon['_source'].get('notes')
        # new_coupon['batchurl'] = coupon['_source'].get('batchurl')
        # new_coupon['from_url'] = coupon['_source'].get('from_url')
        # new_coupon['salesurl'] = coupon['_source'].get('salesurl')
        # new_coupon['shopId'] = coupon['_source'].get('shopId')
        data.append(new_coupon)
    pages = math.ceil(result['hits']['total'] / count)
    next = page + 1 if page < pages else page
    has_next = True if page < pages else False
    r = {'coupons': data, 'next': next, 'pages': pages, 'has_next': has_next}
    return success(r)


@api_v0_1.route('/coupon/pc/unlock', methods=['GET', 'POST'])
@auth_required
def coupon_pc_unlock():
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
    from_url = item['_source']['from_url']
    s = Short_URL.objects(url=from_url).first()
    if s:
        return success(url_for('root.short_url', jid=s.jid, _external=True))
    else:
        data = create_url(from_url)
        if data[0]:
            s = Short_URL()
            sign_hash = hashlib.md5()
            sign_hash.update((current_app.config['SALT'] + from_url).encode('utf-8'))
            s.jid = sign_hash.hexdigest()
            s.url = from_url
            s.create_url = data[1]
            s.update_time = datetime.datetime.utcnow()
            s.save()
            return success(url_for('root.short_url', jid=s.jid, _external=True))
        else:
            return bad_request(data[1])

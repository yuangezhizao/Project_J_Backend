#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
    :Author: yuangezhizao
    :Time: 2019/1/28 0028 23:21
    :Site: http://www.yuangezhizao.cn
    :Copyright: © 2019 yuangezhizao <root@yuangezhizao.cn>
"""
import math
from flask import request

from main.apis.v0_1 import api_v0_1
from main.apis.v0_1.outputs import success, bad_request, not_found
from main.apis.v0_1.user import auth_required
from main.models.good import Good
from main.plugins.extensions import es


@api_v0_1.route('/good', methods=['GET', 'POST'])
@auth_required
def good_index():
    page = request.get_json()['page'] if ((request.get_json() is not None) and ('page' in request.get_json())) else 1
    paginated_goods = Good.objects.order_by('-update_time').paginate(page=page, per_page=10)
    r = []
    for good in paginated_goods.items:
        new_good = {}
        new_good['sku'] = good['sku']
        new_good['title'] = good['title']
        new_good['prize'] = good['price_now']
        new_good['url'] = good['url']
        new_good['img'] = good['img']
        r.append(new_good)
    next = page + 1 if paginated_goods.has_next else page
    r = {'goods': r, 'next': next, 'pages': paginated_goods.pages, 'has_next': paginated_goods.has_next}
    return success(r)


@api_v0_1.route('/good/detail', methods=['GET', 'POST'])
@auth_required
def good_detail():
    try:
        sku = request.get_json()['sku']
    except Exception as e:
        print(e)
        return bad_request('参数错误')
    good = Good.objects(sku=sku).first()
    if good is None:
        return not_found('商品码无效')
    r = {
        'sku': good.sku,
        'price_now': good.price_now,
        'img': good.img,
        'title': good.title.strip(),
        'url': good.url,
        'discountpercent': ('%.2f' % good.discountpercent),
        'jd_price': good.jd_price,
        'buy_count': good.buy_count,
        'his_price': good.his_price,
        'cuxiao': good.cuxiao,
        'coupon_discount': good.coupon_discount,
        'coupon_quota': good.coupon_quota,
        'coupon_url': good.coupon_url
    }
    return success(r)


@api_v0_1.route('/good/search')
def good_search():
    count = int(request.args.get('count', 28)) if (int(request.args.get('count', 28)) in [8, 28]) else 28
    page = int(request.args.get('page', 1)) if (int(request.args.get('page', 1)) < 100) else 100
    content = request.args.get('content', '')
    type = int(request.args.get('type', 1))
    query = {
        'size': count,
        'from': (page - 1) * count
    }
    if content:
        query['query'] = {
            'multi_match': {
                'query': content,
                'fields': ['_id', 'title']
            }
        }
    if type == 2:
        query['sort'] = [{'discountpercent': 'asc'}]
    else:
        query['sort'] = [{'update_time': 'desc'}]
    result = es.search(index='jd', doc_type='projectj_goods', body=query)
    data = []
    for good in result['hits']['hits']:
        if good['_source'].get('title'):
            new_good = {}
            new_good['sku'] = good['_source'].get('sku')
            new_good['price_now'] = good['_source'].get('price_now')
            new_good['img'] = good['_source'].get('img')
            new_good['title'] = good['_source'].get('title').strip()
            new_good['batchCount'] = good['_source'].get('batchCount')
            new_good['discountpercent'] = good['_source'].get('discountpercent')
            new_good['url'] = good['_source'].get('url')
            new_good['discountpercent'] = ('%.2f' % (good['_source'].get('discountpercent')))
            new_good['jd_price'] = good['_source'].get('jd_price')
            new_good['buy_count'] = good['_source'].get('buy_count')
            new_good['his_price'] = good['_source'].get('his_price')
            new_good['cuxiao'] = good['_source'].get('cuxiao')
            new_good['coupon_discount'] = good['_source'].get('coupon_discount')
            new_good['coupon_quota'] = good['_source'].get('coupon_quota')
            new_good['coupon_url'] = good['_source'].get('coupon_url')
            data.append(new_good)
    pages = math.ceil(result['hits']['total'] / count)
    next = page + 1 if page < pages else page
    has_next = True if page < pages else False
    r = {'goods': data, 'next': next, 'pages': pages, 'has_next': has_next}
    return success(r)

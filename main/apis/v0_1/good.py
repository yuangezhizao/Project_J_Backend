#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
    :Author: yuangezhizao
    :Time: 2019/1/28 0028 23:21
    :Site: http://www.yuangezhizao.cn
    :Copyright: © 2019 yuangezhizao <root@yuangezhizao.cn>
"""
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
    Update_time, Disperent, Quota = 1, 2, 3
    # 枚举类型 按照什么排序规则排序
    count_allowed = [8, 28]
    page = int(request.args.get('page', 1))
    s_content = request.args.get('content', '')
    s_type = int(request.args.get('type', 1))
    count = int(request.args.get('count', 28))
    if count not in count_allowed:
        count = 28
    query = {
        'query': {
            'multi_match': {
                'query': s_content,
                'fields': ['_id', 'title']
                # 'fields': ['sku', 'title','jd_price','price_now']
            }
        },
        'size': count,
        'from': (page - 1) * count
    }
    if not s_content:
        query = {
            'size': count,
            'from': (page - 1) * count
        }
    if Update_time == s_type:
        sort = [{'update_time': 'desc'}]
    elif Disperent == s_type:
        sort = [{'discountpercent': 'asc'}]
    # elif Quota == s_type:
    #     sort = [{'quota': 'desc'}]
    else:
        sort = [{'update_time': 'desc'}]
    query['sort'] = sort
    r = es.search(index='jd', doc_type='projectj_goods', body=query)
    data = []
    for item in list(r['hits']['hits']):
        data.append({
            '_id': item.get('_id'),
            # 'sort': item.get('sort'),
            # '_type': item.get('_type'),
            # '_source': {
            'sku': item['_source'].get('sku'),
            'title': item['_source'].get('title'),
            'img': item['_source'].get('img'),
            'jd_price': item['_source'].get('jd_price'),
            'price_now': item['_source'].get('price_now'),
        })
    result = {  # 'total': r['hits']['hits']}
        'result': data}
    return success(result)

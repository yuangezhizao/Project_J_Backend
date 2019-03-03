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

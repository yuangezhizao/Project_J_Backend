#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
    :Author: yuangezhizao
    :Time: 2019/1/28 0028 13:34
    :Site: http://www.yuangezhizao.cn
    :Copyright: © 2019 yuangezhizao <root@yuangezhizao.cn>
"""
from flask import request, g

from main.apis.v0_1 import api_v0_1
from main.apis.v0_1.outputs import success, bad_request, not_found
from main.apis.v0_1.user import auth_required
from main.models.coupon import Coupon


@api_v0_1.route('/coupon', methods=['GET', 'POST'])
@auth_required
def coupon_index():
    page = request.get_json()['page'] if ((request.get_json() is not None) and ('page' in request.get_json())) else 1
    paginated_coupons = Coupon.objects.paginate(page=page, per_page=10)
    r = []
    for coupon in paginated_coupons.items:
        new_coupon = {}
        new_coupon['key'] = coupon['key']
        new_coupon['name'] = coupon['name']
        new_coupon['strength'] = coupon['strength']
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
    result = g.user.unlock_action(key)
    if result != 'Success':
        return result
    r = {
        'key': coupon.key,
        'name': coupon.name,
        'strength': coupon.strength,
        # 'act_url': coupon.act_url,
        # 'url': coupon.url
    }
    return success(r)

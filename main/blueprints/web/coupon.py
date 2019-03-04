#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
    :Author: yuangezhizao
    :Time: 2019/2/28 0028 20:11
    :Site: https://www.yuangezhizao.cn
    :Copyright: © 2019 yuangezhizao <root@yuangezhizao.cn>
"""
import datetime

from flask import request

from main.apis.v0_1.outputs import success, bad_request, not_found, error
from main.models.coupon import Coupon
from main.models.coupon_orig import Coupon_Orig
from . import web_bp


@web_bp.route('/coupon', methods=['GET', 'POST'])
def coupon_index():
    page = int(request.args.get('page')) if (
            (request.args.get('page') is not None) and (request.args.get('page') != '')) else 1
    paginated_coupons = Coupon_Orig.objects(limitStr__exists=True).order_by('-update_time').paginate(page=page,
                                                                                                     per_page=10)
    r = []
    for coupon in paginated_coupons.items:
        new_coupon = {}
        new_coupon['key'] = coupon['key']
        new_coupon['limitStr'] = coupon['limitStr']
        new_coupon['discount'] = coupon['discount']
        new_coupon['discountpercent'] = coupon['discountpercent']
        new_coupon['batchId'] = coupon['batchId']
        new_coupon['batchCount'] = coupon['batchCount']
        new_coupon['beginTime'] = coupon['beginTime'].strftime('%Y-%m-%d %H:%M:%S')
        new_coupon['endTime'] = coupon['endTime'].strftime('%Y-%m-%d %H:%M:%S')
        new_coupon['update_time'] = coupon['update_time'].strftime('%Y-%m-%d %H:%M:%S')
        new_coupon['status'] = True if Coupon.objects(key=coupon['key']).first() is not None else False
        new_coupon['coupon_name'] = '满 {0} 减 {1}'.format(coupon['quota'], coupon['discount'])
        new_coupon['url'] = coupon['url']
        new_coupon['salesurl'] = coupon['salesurl']
        new_coupon['batchurl'] = coupon['batchurl']
        new_coupon['from_url'] = coupon['from_url']
        r.append(new_coupon)
    next = page + 1 if paginated_coupons.has_next else page
    r = {'coupons': r, 'next': next, 'pages': paginated_coupons.pages, 'has_next': paginated_coupons.has_next}
    return success(r)


@web_bp.route('/coupon/show', methods=['GET', 'POST'])
def coupon_show():
    try:
        key = request.form['key']
    except Exception as e:
        print(e)
        return bad_request('参数错误')
    coupon_orig = Coupon_Orig.objects(key=key).first()
    if coupon_orig is None:
        return not_found('优惠券码无效')
    coupon = Coupon()
    for k in coupon_orig:
        coupon[k] = coupon_orig[k]
    coupon['update_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    coupon.save()
    return success('ok')


@web_bp.route('/coupon/unshow', methods=['GET', 'POST'])
def coupon_unshow():
    try:
        key = request.form['key']
    except Exception as e:
        print(e)
        return bad_request('参数错误')
    coupon_orig = Coupon.objects(key=key).first()
    if coupon_orig is None:
        return not_found('优惠券码无效')
    else:
        coupon_orig.delete()
        return success('ok')


@web_bp.route('/coupon/search', methods=['GET', 'POST'])
def coupon_search():
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

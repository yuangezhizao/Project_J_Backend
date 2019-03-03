#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
    :Author: yuangezhizao
    :Time: 2019/2/28 0028 20:11
    :Site: https://www.yuangezhizao.cn
    :Copyright: © 2019 yuangezhizao <root@yuangezhizao.cn>
"""
import math

import pymongo
from flask import request, current_app

from main.apis.v0_1.outputs import success
from . import web_bp


@web_bp.route('/coupon', methods=['GET', 'POST'])
def coupon_index():
    conn = pymongo.MongoClient(current_app.config['MONGODB_SETTINGS']['host'])['jd']
    page = int(request.args.get('page')) if (
            (request.args.get('page') is not None) and (request.args.get('page') != '')) else 1
    coupon_count = conn['coupon_detail'].count()
    pages = int(math.ceil(float(coupon_count) / 10))
    paginated_coupons = conn['coupon_detail'].find().sort('update_time', pymongo.DESCENDING).skip(page - 1).limit(10)
    r = []
    for coupon in paginated_coupons:
        new_coupon = {}
        new_coupon['key'] = coupon['key']
        new_coupon['from_title'] = coupon['from_title'].strip()
        new_coupon['update_time'] = coupon['update_time'].strftime('%Y-%m-%d %H:%M:%S')
        new_coupon['from'] = coupon['from']

        new_coupon['limitStr'] = coupon['limitStr'] if 'limitStr' in coupon else ''
        new_coupon['quota'] = coupon['quota'] if 'quota' in coupon else ''
        new_coupon['discount'] = coupon['discount'] if 'discount' in coupon else ''
        new_coupon['batchCount'] = coupon['batchCount'] if 'batchCount' in coupon else ''
        new_coupon['discountpercent'] = coupon['discountpercent'] if 'discountpercent' in coupon else ''
        new_coupon['salesurl'] = coupon['salesurl'] if 'salesurl' in coupon else ''
        new_coupon['url'] = coupon['url'] if 'url' in coupon else ''
        new_coupon['batchurl'] = coupon['batchurl'] if 'batchurl' in coupon else ''
        r.append(new_coupon)
    next = page + 1 if (10 * page < coupon_count) else page
    has_next = True if (10 * page <= coupon_count) else False
    r = {'goods': r, 'next': next, 'pages': pages, 'has_next': has_next}
    return success(r)

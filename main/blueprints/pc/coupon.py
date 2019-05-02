#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
    :Author: yuangezhizao
    :Time: 2019/5/2 0002 10:22
    :Site: https://www.yuangezhizao.cn
    :Copyright: © 2019 yuangezhizao <root@yuangezhizao.cn>
"""
from flask import request

from main.apis.v0_1.outputs import success, bad_request, not_found
from main.plugins.extensions import es
from . import pc_bp


@pc_bp.route('/coupon/unlock', methods=['GET', 'POST'])
def coupon_unlock():
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

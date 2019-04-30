#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
    :Co-authored-by: liyanzhe
    :Author: yuangezhizao
    :Time: 2019/4/30 0030 13:14
    :Site: https://www.yuangezhizao.cn
    :Copyright: © 2019 liyanzhe <liyanzhe@igengmei.com>
    :Copyright: © 2019 yuangezhizao <root@yuangezhizao.cn>
"""
from flask import request

from main.apis.v0_1 import api_v0_1
from main.apis.v0_1.outputs import success
from main.plugins.extensions import es


@api_v0_1.route('/item/search', methods=['GET'])
def search_item():
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
        query = {}
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

#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
    :Author: yuangezhizao
    :Time: 2019/2/17 0017 16:31
    :Site: https://www.yuangezhizao.cn
    :Copyright: © 2019 yuangezhizao <root@yuangezhizao.cn>
"""
from flask import request

from main.apis.v0_1.outputs import success, bad_request
from . import web_bp


@web_bp.route('/wx/user')
def wx_user_index():
    from main.models.user import WX_User
    page = int(request.args.get('page')) if (
            (request.args.get('page') is not None) and (request.args.get('page') != '')) else 1
    # TODO：wtforms
    paginated_users = WX_User.objects().order_by('member_since').paginate(page=page, per_page=10)
    r = []
    for user in paginated_users.items:
        new_user = {}
        new_user['uid'] = user['uid']
        new_user['nickName'] = user['userinfo']['nickName']
        new_user['points'] = user['points']
        new_user['member_since'] = user['member_since'].strftime('%Y-%m-%d %H:%M:%S')
        r.append(new_user)
    next = page + 1 if paginated_users.has_next else page
    r = {'users': r, 'next': next, 'pages': paginated_users.pages, 'has_next': paginated_users.has_next}
    return success(r)


@web_bp.route('/wx/user/search', methods=['GET', 'POST'])
def wx_user_search():
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

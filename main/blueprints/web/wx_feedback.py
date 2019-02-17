#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
    :Author: yuangezhizao
    :Time: 2019/2/17 0017 15:24
    :Site: https://www.yuangezhizao.cn
    :Copyright: © 2019 yuangezhizao <root@yuangezhizao.cn>
"""
from flask import request

from main.apis.v0_1.outputs import success
from main.models.feedback import WX_Feedback
from main.models.user import WX_User
from . import web_bp


@web_bp.route('/wx/feedback')
def wx_feedback_index():
    page = int(request.args.get('page')) if (
            (request.args.get('page') is not None) and (request.args.get('page') != '')) else 1
    # TODO：wtforms
    paginated_feedbacks = WX_Feedback.objects().order_by('insert_time').paginate(page=page, per_page=10)
    r = []
    for feedback in paginated_feedbacks.items:
        new_feedback = {}
        new_feedback['id'] = str(feedback['id'])
        new_feedback['nickName'] = WX_User.objects(uid=(feedback['uid'])).first().userinfo['nickName']
        new_feedback['msg'] = feedback['msg']
        new_feedback['insert_time'] = feedback['insert_time'].strftime('%Y-%m-%d %H:%M:%S')
        r.append(new_feedback)
    next = page + 1 if paginated_feedbacks.has_next else page
    r = {'feedbacks': r, 'next': next, 'pages': paginated_feedbacks.pages, 'has_next': paginated_feedbacks.has_next}
    return success(r)

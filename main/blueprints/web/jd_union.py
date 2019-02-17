#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
    :Author: yuangezhizao
    :Time: 2019/2/13 0013 22:33
    :Site: https://www.yuangezhizao.cn
    :Copyright: © 2019 yuangezhizao <root@yuangezhizao.cn>
"""
from flask import request, jsonify

from main.apis.v0_1.outputs import success
from main.models.socialmedia import Socialmedia
from . import web_bp


@web_bp.route('/jd_union/create_url')
def jd_union_create_url():
    from main.services.jd_union.web_api import WebApi
    web_api = WebApi()
    # RuntimeError: Working outside of application context.
    social_media_id = request.args.get('social_media_id')
    sub_pid = request.args.get('sub_pid')
    channel_url = request.args.get('channel_url')
    return jsonify(web_api.create_url(social_media_id, sub_pid, channel_url))


@web_bp.route('/jd_union/create_social_media')
def jd_union_create_social_media():
    from main.services.jd_union.web_api import WebApi
    web_api = WebApi()
    channel_url = request.args.get('channel_url')
    account = request.args.get('account')
    social_media_name = request.args.get('social_media_name')
    return jsonify(web_api.create_social_media(channel_url, account, social_media_name))


@web_bp.route('/jd_union/remove_social_media')
def jd_union_remove_social_media():
    from main.services.jd_union.web_api import WebApi
    web_api = WebApi()
    social_media_id = request.args.get('social_media_id')
    return jsonify(web_api.remove_social_media(social_media_id))


@web_bp.route('/jd_union/get_social_media_list')
def jd_union_get_social_media_list():
    page = int(request.args.get('page')) if (
            (request.args.get('page') is not None) and (request.args.get('page') != '')) else 1
    # TODO：wtforms
    social_media_list = Socialmedia.objects().order_by('createTime').paginate(page=page, per_page=10)
    r = []
    for social_media in social_media_list.items:
        new_social_media = {}
        new_social_media['id'] = int(social_media['id'])
        new_social_media['mediaName'] = social_media['mediaName']
        new_social_media['homeUrl'] = social_media['homeUrl']
        new_social_media['loginAccount'] = social_media['loginAccount']
        new_social_media['createTime'] = social_media['createTime']  # .strftime('%Y-%m-%d %H:%M:%S')
        new_social_media['updateTime'] = social_media['updateTime']  # .strftime('%Y-%m-%d %H:%M:%S')
        r.append(new_social_media)
    next = page + 1 if social_media_list.has_next else page
    r = {'social_media_list': r, 'next': next, 'pages': social_media_list.pages, 'has_next': social_media_list.has_next}
    return success(r)


@web_bp.route('/jd_union/create_social_media_loc')
def jd_union_create_social_media_loc():
    from main.services.jd_union.web_api import WebApi
    web_api = WebApi()
    social_media_id = request.args.get('social_media_id')
    sub_name = request.args.get('sub_name')
    return jsonify(web_api.create_social_media_loc(social_media_id, sub_name))


@web_bp.route('/jd_union/remove_social_media_loc')
def jd_union_remove_social_media_loc():
    from main.services.jd_union.web_api import WebApi
    web_api = WebApi()
    sub_pid = request.args.get('sub_pid')
    return jsonify(web_api.remove_social_media_loc(sub_pid))


@web_bp.route('/jd_union/get_social_media_loc_list')
def jd_union_get_social_media_loc_list():
    from main.services.jd_union.web_api import WebApi
    web_api = WebApi()
    social_media_id = request.args.get('social_media_id')
    page = request.args.get('page', 1)
    pass


@web_bp.route('/jd_union/get_social_media_by_args')
def jd_union_get_social_media_by_args():
    from main.services.jd_union.web_api import WebApi
    web_api = WebApi()
    social_media_id = request.args.get('social_media_id')
    social_media_name = request.args.get('social_media_name')
    channel_url = request.args.get('channel_url')
    account = request.args.get('account')
    return jsonify(web_api.get_social_media_by_args(social_media_id, social_media_name, channel_url, account))


@web_bp.route('/jd_union/get_social_media_loc_by_args')
def jd_union_get_social_media_loc_by_args():
    from main.services.jd_union.web_api import WebApi
    web_api = WebApi()
    social_media_id = request.args.get('social_media_id')
    sub_name = request.args.get('sub_name')
    return jsonify(web_api.get_social_media_loc_by_args(social_media_id, sub_name))

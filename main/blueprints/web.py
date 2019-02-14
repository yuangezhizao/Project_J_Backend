#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
    :Author: yuangezhizao
    :Time: 2019/2/13 0013 22:33
    :Site: https://www.yuangezhizao.cn
    :Copyright: © 2019 yuangezhizao <root@yuangezhizao.cn>
"""
from flask import Blueprint, request, jsonify

web_bp = Blueprint('web', __name__)


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


@web_bp.route('/jd_union/refresh_social_media_list')
def jd_union_refresh_social_media_list():
    from main.services.jd_union.web_api import WebApi
    web_api = WebApi()
    page = request.args.get('page', 1)
    return jsonify(web_api.refresh_social_media_list(page))


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


@web_bp.route('/jd_union/refresh_social_media_loc_list')
def jd_union_refresh_social_media_loc_list():
    from main.services.jd_union.web_api import WebApi
    web_api = WebApi()
    social_media_id = request.args.get('social_media_id')
    page = request.args.get('page', 1)
    return jsonify(web_api.refresh_social_media_loc_list(social_media_id, page))


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

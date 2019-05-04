#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
    :Author: yuangezhizao
    :Time: 2019/1/25 0025 21:50
    :Site: http://www.yuangezhizao.cn
    :Copyright: © 2019 yuangezhizao <root@yuangezhizao.cn>
"""
import datetime
import hashlib

from flask import Blueprint, render_template, redirect, request, url_for

from main.apis.v0_1.outputs import not_found, bad_request
from main.models.short_url import Short_URL

root_bp = Blueprint('root', __name__)


@root_bp.route('/')
def hello_world():
    return render_template('index.html')


@root_bp.route('/create_url')
def create_url():
    from main.services.jd_union.open_api import create_url
    common_url = request.args.get('common_url')
    if not common_url:
        return bad_request(data='参数不完整')
    data = create_url(common_url)
    if data[0]:
        s = Short_URL()
        sign_hash = hashlib.md5()
        sign_hash.update(data[1].encode('utf-8'))
        s.jid = sign_hash.hexdigest()
        s.url = data[1]
        s.update_time = datetime.datetime.utcnow()
        s.save()
        return url_for('root.short_url', jid=s.jid, _external=True)
    else:
        return bad_request(data[1])


@root_bp.route('/s/<jid>')
def short_url(jid):
    from main.services.jd_union.open_api import create_url
    s = Short_URL.objects(jid=jid).first()
    if s is None:
        return not_found('键无效')
    if 'union-click' in s.url:
        return redirect(s.url)
    data = create_url(s.url)
    if data[0]:
        s.url = data[1]
        s.save()
        return redirect(data[1])
    else:
        return bad_request(data[1])

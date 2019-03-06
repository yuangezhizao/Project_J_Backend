#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
    :Author: yuangezhizao
    :Time: 2019/3/6 0006 14:51
    :Site: https://www.yuangezhizao.cn
    :Copyright: © 2019 yuangezhizao <root@yuangezhizao.cn>
"""
from flask import request, redirect

from main.models.coupon_orig import Coupon_Orig
from main.models.good import Good
from main.models.lottery import Lottery
from . import web_bp


@web_bp.route('/misc')
def misc_index():
    sku = request.args.get('sku')
    key = request.args.get('key')
    lotteryCode = request.args.get('lotteryCode')
    if sku:
        good = Good.objects(sku=sku).first()
        return redirect(good.url)
    elif key:
        coupon = Coupon_Orig.objects(key=key).first()
        return redirect(coupon.url)
    elif lotteryCode:
        lottery = Lottery.objects(lotteryCode=lotteryCode).first()
        return redirect(lottery.url)

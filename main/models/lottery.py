#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
    :Author: yuangezhizao
    :Time: 2019/1/28 0028 13:32
    :Site: http://www.yuangezhizao.cn
    :Copyright: © 2019 yuangezhizao <root@yuangezhizao.cn>
"""
from main.plugins.extensions import db


class Lottery(db.Document):
    meta = {
        'collection': 'lottery_detail'
    }
    lotteryCode = db.StringField(required=True, primary_key=True)  # 抽奖代码
    lotteryName = db.StringField(required=True)  # 抽奖名称
    beginTime = db.DateTimeField(required=True)  # 开始时间
    endTime = db.DateTimeField(required=True)  # 结束时间
    lotteryPrize = db.ListField(required=True)  # 抽奖奖品
    url = db.StringField(required=True)  # 抽奖地址

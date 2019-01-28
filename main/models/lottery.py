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
        'collection': 'lottery_detail',
        'indexes': [
            {
                'fields': ['$lotteryCode', ],
                'default_language': 'english',
            }
        ]
    }
    lotteryCode = db.StringField(required=True, primary_key=True)  # 抽奖代码
    lotteryName = db.StringField(required=True)  # 抽奖名称
    beginTime = db.DateTimeField(required=True)  # 开始时间
    endTime = db.DateTimeField(required=True)  # 结束时间
    lotteryPrize = db.ListField(required=True)  # 抽奖奖品
    url = db.StringField(required=True)  # 抽奖地址
    # 路由处使用 paginate，则模型必须填写完整字段
    update_time = db.DateTimeField(required=True)  # 插入时间
    accessMethod = db.IntField(required=True)  # 略
    jbeanAmount = db.IntField(required=True)  # 略
    promptImg = db.StringField(required=True)  # 图片
    lotteryCreator = db.StringField(required=True)  # 抽奖创建者

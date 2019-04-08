#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
    :Author: yuangezhizao
    :Time: 2019/4/1 0001 16:01
    :Site: https://www.yuangezhizao.cn
    :Copyright: © 2019 yuangezhizao <root@yuangezhizao.cn>
"""
# https://github.com/dongweiming/wechat-admin/blob/master/libs/wx.py?1554107012255#L28-L36

from wxpy import Bot


def get_bot():
    bot = Bot(cache_path=True, qr_path='/home/ubuntu/projectj_mp_backend/main/static/wx.png', console_qr=False)
    bot.enable_puid()
    bot.messages.max_history = 0
    return bot

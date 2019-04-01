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
    bot = Bot('bot.pkl', qr_path='wx.png', console_qr=None)
    bot.enable_puid()
    bot.messages.max_history = 0
    return bot

#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
    :Author: yuangezhizao
    :Time: 2019/4/5 0005 9:58
    :Site: https://www.yuangezhizao.cn
    :Copyright: © 2019 yuangezhizao <root@yuangezhizao.cn>
"""
from werkzeug.local import LocalStack, LocalProxy


def _find_bot():
    from main.services.wechat.wx import get_bot
    top = _wx_ctx_stack.top
    if top is None:
        top = get_bot()
        _wx_ctx_stack.push(top)
    return top


_wx_ctx_stack = LocalStack()
current_bot = LocalProxy(_find_bot)

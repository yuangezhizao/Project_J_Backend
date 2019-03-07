#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
    :Author: yuangezhizao
    :Time: 2019/1/25 0025 22:43
    :Site: http://www.yuangezhizao.cn
    :Copyright: © 2019 yuangezhizao <root@yuangezhizao.cn>
"""
from flask import url_for

from tests.base import BaseTestCase


class RootTestCase(BaseTestCase):

    def test_hello_world_page(self):
        response = self.client.get(url_for('root.hello_world'))
        data = response.get_data(as_text=True)
        # self.assertIn('Hello, Flask!', data)

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


class MainTestCase(BaseTestCase):

    def test_hello_world_page(self):
        response = self.client.get(url_for('main.hello_world'))
        data = response.get_data(as_text=True)
        self.assertIn('Hello, Flask!', data)

    def test_jd_verify(self):
        response = self.client.get(url_for('main.jd_verify'))
        data = response.get_data(as_text=True)
        self.assertIn('e95d2f4a675fe6f2b231093ef0892219c03e13e310499f23', data)

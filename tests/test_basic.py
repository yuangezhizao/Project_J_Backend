#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
    :Author: yuangezhizao
    :Time: 2019/1/25 0025 22:42
    :Site: http://www.yuangezhizao.cn
    :Copyright: © 2019 yuangezhizao <root@yuangezhizao.cn>
"""
from flask import current_app

from tests.base import BaseTestCase


class BasicTestCase(BaseTestCase):

    def test_app_exist(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])

    def test_404_error(self):
        response = self.client.get('/foo')
        data = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 404)

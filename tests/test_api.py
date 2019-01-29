#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
    :Author: yuangezhizao
    :Time: 2019/1/29 0029 17:11
    :Site: http://www.yuangezhizao.cn
    :Copyright: © 2019 yuangezhizao <root@yuangezhizao.cn>
"""

from tests.base import BaseTestCase


class APITestCase(BaseTestCase):

    def test_info_points(self):
        response = self.client.get('api/v0_1/info/points')
        data = response.get_json()
        self.assertEqual(data['code'], 0)

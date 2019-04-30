#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
    :Author: yuangezhizao
    :Time: 2019/1/24 0024 19:46
    :Site: http://www.yuangezhizao.cn
    :Copyright: © 2019 yuangezhizao <root@yuangezhizao.cn>
"""
import os

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', None)
    MONGODB_SETTINGS = {
        'db': os.getenv('MONGODB_SETTINGS_DB', None),
        'host': os.getenv('MONGODB_SETTINGS_HOST', None),
        'port': 27017,
        'username': os.getenv('MONGODB_SETTINGS_USERNAME', None),
        'password': os.getenv('MONGODB_SETTINGS_PASSWORD', None),
        'connect': False
    }
    ES_SETTINGS = {
        'host': os.getenv('ES_SETTINGS_HOST', None),
        'port': 9200
    }
    APPID = os.getenv('APPID', None)
    APPSECRET = os.getenv('APPSECRET', None)
    FAKE_NUM = os.getenv('FAKE_NUM', None)
    SENTRY_DSN = os.getenv('SENTRY_DSN', None)
    JD_UNION_APP_KEY = os.getenv('JD_UNION_APP_KEY', None)
    JD_UNION_APP_SECRET = os.getenv('JD_UNION_APP_SECRET', None)
    JD_UNION_SITE_ID = os.getenv('JD_UNION_SITE_ID', None)
    WX_OPEN_APP_ID = os.getenv('WX_OPEN_APP_ID', None)
    WX_OPEN_APP_SECRET = os.getenv('WX_OPEN_APP_SECRET', None)


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    TESTING = True


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': ProductionConfig
}

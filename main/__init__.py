#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
    :Author: yuangezhizao
    :Time: 2019/1/24 0024 19:33
    :Site: http://www.yuangezhizao.cn
    :Copyright: © 2019 yuangezhizao <root@yuangezhizao.cn>
"""
import os

from flask import Flask

from main.apis.v0_1 import api_v0_1
from main.blueprints.main import main_bp
from main.plugins.extensions import db
from main.settings import config


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'default')

    app = Flask(__name__, static_folder='static')
    app.config.from_object(config[config_name])

    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_commands(app)
    register_template_context(app)

    return app


def register_extensions(app):
    db.init_app(app)


def register_blueprints(app):
    app.register_blueprint(main_bp, url_prefix='/')
    app.register_blueprint(api_v0_1, url_prefix='/api/v0_1')


def register_errorhandlers(app):
    pass


def register_commands(app):
    pass


def register_template_context(app):
    pass

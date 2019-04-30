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
from raven.contrib.flask import Sentry

from main.apis.v0_1 import api_v0_1
from main.blueprints.pc import pc_bp
from main.blueprints.root import root_bp
from main.blueprints.web import web_bp
from main.plugins.extensions import db, es
from main.settings import config


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'default')

    app = Flask(__name__, static_url_path='')
    app.config.from_object(config[config_name])

    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_commands(app)
    register_template_context(app)

    return app


def register_extensions(app):
    sentry = Sentry(app, dsn=app.config['SENTRY_DSN'])
    sentry.init_app(app)
    db.init_app(app)
    es.init_app(app)


def register_blueprints(app):
    app.register_blueprint(root_bp, url_prefix='/')
    app.register_blueprint(api_v0_1, url_prefix='/api/v0_1')
    app.register_blueprint(web_bp, url_prefix='/web')
    app.register_blueprint(pc_bp, url_prefix='/pc')


def register_errorhandlers(app):
    pass


def register_commands(app):
    pass


def register_template_context(app):
    pass

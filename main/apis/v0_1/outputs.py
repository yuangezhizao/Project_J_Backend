#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
    :Author: yuangezhizao
    :Time: 2019/1/26 0026 11:59
    :Site: http://www.yuangezhizao.cn
    :Copyright: © 2019 yuangezhizao <root@yuangezhizao.cn>
"""
from flask import jsonify

from main.apis.v0_1 import api_v0_1


def success(data, message='Success'):
    response = jsonify({'code': 0, 'message': message, 'data': data, 'ttl': 1})
    response.status_code = 200
    return response


def bad_request(data, message='Bad request'):
    response = jsonify({'code': -400, 'message': message, 'data': data, 'ttl': 1})
    response.status_code = 400
    return response


def unauthorized(data, message='Unauthorized'):
    response = jsonify({'code': -401, 'message': message, 'data': data, 'ttl': 1})
    response.status_code = 401
    return response


def forbidden(data, message='Forbidden'):
    response = jsonify({'code': -403, 'message': message, 'data': data, 'ttl': 1})
    response.status_code = 403
    return response


def not_found(data, message='Not Found'):
    response = jsonify({'code': -404, 'message': message, 'data': data, 'ttl': 1})
    response.status_code = 404
    return response


def error(data, message='Error'):
    response = jsonify({'code': -500, 'message': message, 'data': data, 'ttl': 1})
    response.status_code = 500
    # app.logger.error('500：%s', (message))
    # TODO：error content temp solve, just use in where it is
    return response


def unavailable(data, message='Service Unavailable'):
    response = jsonify({'code': -503, 'message': message, 'data': data, 'ttl': 600})
    response.status_code = 503
    return response


class ValidationError(ValueError):
    pass


@api_v0_1.errorhandler(ValidationError)
def validation_error(e):
    return bad_request(400)

# TODO：**kwargs
# from werkzeug.http import HTTP_STATUS_CODES
#
#
# def api_abort(code, message=None, **kwargs):
#     if message is None:
#         message = HTTP_STATUS_CODES.get(code, '')
#
#     response = jsonify(code=code, message=message, **kwargs)
#     response.status_code = code
#     return response  # You can also just return (response, code) tuple
#
#
# @api_v0_1.errorhandler(ValidationError)
# def validation_error(e):
#     return api_abort(400, e.args[0])

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from flask import make_response


def get_response(data=None, msg=None, cede=None):
    resp = make_response()
    resp.headers['Content-Type'] = 'application/json;charset=UTF-8'
    resp.response = json.dumps({
        'code': cede,
        'data': data,
        'message': msg
    })
    return resp


def mark_success(data=None, msg='成功'):
    return get_response(data, msg, 200)


def mark_fail(data=None, msg='失败'):
    return get_response(data, msg, 500)


def mark_not_login(data=None, msg='登录失效'):
    return get_response(data, msg, 1000)
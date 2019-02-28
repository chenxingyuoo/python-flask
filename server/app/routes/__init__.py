#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Blueprint, request
from flask_wtf.csrf import validate_csrf
from wtforms import ValidationError
from ..utils import mark_not_login
from ..redis_init import client
import json

# 实例化 Blueprint 类，两个参数分别为蓝本的名字和蓝本所在包或模块，第二个通常填 __name__ 即可
routes = Blueprint('routes', __name__)

from . import user


@routes.before_request
def before_request():

    if request.path != '/api/user/login' and request.path != '/':

        current_csrf_token = request.cookies.get('csrf_token', '')
        user = client.get(current_csrf_token)
        if  user is None:
            return mark_not_login(msg='token无效')
        user = json.loads(user)
        username = user['username']

        csrf_token = str(client.get(username + '_csrf_token'), encoding='utf-8')
        if csrf_token != current_csrf_token:
            return mark_not_login(msg='您的账号在别处登录了')

        try:
            validate_csrf(csrf_token, secret_key=username)
        except ValidationError as e:
            client.delete(csrf_token)
            return mark_not_login(msg=e.args[0])

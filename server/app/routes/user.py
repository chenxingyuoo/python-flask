#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import render_template, request, redirect, make_response
# 导入蓝本 main
from . import routes
from ..models.users import Users
import json
# import jwt
from ..redis_init import client
# 导入生成 csrf_token 值的函数
from flask_wtf.csrf import generate_csrf
from ..utils import mark_success, mark_fail

users = Users()

@routes.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@routes.route('/user/info', methods=['GET'])
def user_info():
    try:
        current_csrf_token = request.cookies.get('csrf_token')
        user = client.get(current_csrf_token)
        return mark_success(json.loads(user))
    except Exception as e:
        return mark_fail(msg=e.args[0])

@routes.route('/user/login', methods=['POST'])
def user_login():
    username = request.json['username'] or ''
    password = request.json['password'] or ''

    try:
        user = users.find_one_by_where({'username': username, 'password': password})
        if user is None:
            return mark_fail(msg='用户名或密码错误')

        # global encoded
        # encoded = jwt.encode({'some': 'payload'}, 'secret', algorithm='HS256')
        # print(str(encoded, encoding='utf-8'))

        # 调用函数生成 csrf_token
        csrf_token = generate_csrf(secret_key=username)

        print(client.keys())

        user_csrf_token_key = username + '_csrf_token'

        client.set(csrf_token, json.dumps(user), 7200)
        client.set(user_csrf_token_key, csrf_token, 7200)

        user['token'] = csrf_token
        # client.set(csrf_token, json.dumps(user))
        # client.expire(csrf_token, 100)

        # 为用户设置cookie值为csrf_token 防止csrf攻击
        resp = make_response()
        resp.set_cookie('csrf_token', csrf_token)
        resp.response = json.dumps({
            'code': 200,
            'data': user,
            'message': '登录成功'
        })
        return resp
    except Exception as e:
        return mark_fail(msg=e.args[0])


@routes.route('/user/list', methods=['GET'])
def user_list():
    currentPage = int(request.args.get('currentPage'))
    pageSize = int(request.args.get('pageSize'))
    keyword = request.args.get('keyword', '')

    try:
        filter = {'$regex': keyword}
        users_data = users.find_all(currentPage=currentPage, pageSize=pageSize, where={'username': filter})
        return mark_success(users_data)
    except Exception as e:
        return mark_fail(msg=e.args[0])

@routes.route('/user/save', methods=['POST'])
def user_save_post():
    id = request.json['id']
    username = request.json['username']
    password = request.json['password']
    try:
        user = users.find_one_by_where({'username': username})
        if user is not None:
            return mark_fail(msg='用户已存在')

        if id is None:
            users.insert_one({'username': username, 'password': password})
        else:
            users.find_one_and_update(id, {'username': username, 'password': password})

        return mark_success()
    except Exception as e:
        return mark_fail(msg=e.args[0])


@routes.route('/user/delete', methods=['POST'])
def user_delete_post():
    id = request.json['id']
    try:
        users.find_one_and_delete(id)
        return mark_success()
    except Exception as e:
        print(e)
        return mark_fail(msg=e.args[0])
    finally:
        print('finally...')


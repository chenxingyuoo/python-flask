#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import render_template, request, redirect, make_response
# 导入蓝本 main
from . import routes
from ..models.users import Users
import json
# import jwt
from ..my_redis import redis_db0
# 导入生成 csrf_token 值的函数
from flask_wtf.csrf import generate_csrf
from ..utils import mark_success, mark_fail

users = Users()


@routes.route('/api/user/login', methods=['POST'])
def user_login():
    username = request.json['username'] or ''
    password = request.json['password'] or ''

    user = users.find_one_by_where({'username': username, 'password': password})
    if user is None:
        return mark_fail(msg='用户名或密码错误')

    # global encoded
    # encoded = jwt.encode({'some': 'payload'}, 'secret', algorithm='HS256')
    # print(str(encoded, encoding='utf-8'))

    # 调用函数生成 csrf_token
    csrf_token = generate_csrf(secret_key=username)

    print(redis_db0.keys())

    # for item in redis_db0.keys():
    #     current = redis_db0.get(item)
    #     currentUser = redis_db0.get(current)
    #     # current = json.loads(redis_db0.get(str(item)))
    #     if current['username'] == user['username']:
    #         redis_db0.delete(item)

    user_csrf_token_key = username + '_csrf_token'

    redis_db0.set(csrf_token, json.dumps(user), 7200)
    redis_db0.set(user_csrf_token_key, csrf_token, 7200)

    # redis_db0.set(csrf_token, json.dumps(user))
    # if redis_db0.get(user_csrf_token_key):
    #    redis_db0.delete(user_csrf_token_key)

    user['csrf_token'] = csrf_token
    # redis_db0.set(csrf_token, json.dumps(user))
    # redis_db0.expire(csrf_token, 100)

    # 为用户设置cookie值为csrf_token 防止csrf攻击
    resp = make_response()
    resp.set_cookie('csrf_token', csrf_token)
    resp.response = json.dumps({
        'code': 200,
        'data': user,
        'message': '登录成功'
    })
    return resp


@routes.route('/', methods=['GET'])
def index():
    global encoded

    currentPage = int(request.args.get('currentPage', 1))
    pageSize = int(request.args.get('pageSize', 2))
    users_data = users.find_all(currentPage=currentPage, pageSize=pageSize)

    # resp = make_response()
    # resp.headers['Content-Type'] = 'application/json'
    # resp.response = users_data
    # return resp
    return render_template('index.html')


@routes.route('/api/user/list', methods=['GET'])
def user_list():
    currentPage = int(request.args.get('currentPage', 1))
    pageSize = int(request.args.get('pageSize', 2))
    users_data = users.find_all(currentPage=currentPage, pageSize=pageSize)
    return mark_success(users_data)


@routes.route('/user/create', methods=['GET'])
def user_create():
    return render_template('user/create.html')


@routes.route('/user/create', methods=['POST'])
def user_create_post():
    username = request.form['username']
    password = request.form['password']
    users.insert_one({'username': username, 'password': password})
    return redirect('/')


@routes.route('/user/update/<id>', methods=['GET'])
def user_update(id):
    user_info = users.find_one(id)
    return render_template('user/update.html', user_info=user_info)


@routes.route('/user/update', methods=['POST'])
def user_update_post():
    id = request.form['id']
    username = request.form['username']
    password = request.form['password']
    users.find_one_and_update(id, {'username': username, 'password': password})
    return redirect('/')


@routes.route('/user/delete/<id>', methods=['GET'])
def user_delete(id):
    print(id, request)
    users.find_one_and_delete(id)
    return redirect(request.referrer)


@routes.route('/api/user/delete', methods=['POST'])
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


@routes.route('/user/info/<id>', methods=['GET'])
def user_info(id):
    user_info = users.find_one(id)
    return render_template('user/info.html', user_info=user_info)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, request
# from . import models
from .routes import routes as routes_blueprint
from .models import orm

def create_app():
    # orm.connection(host='127.0.0.1', port=3306)
    app = Flask(__name__, static_url_path=None, static_folder='static', template_folder="./static")
    app.config['SECRET_KEY'] = 'xxx'
    app.register_blueprint(routes_blueprint)
    # app.wsgi_app = MiddleWare(app.wsgi_app)
    return app
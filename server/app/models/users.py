#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .orm import Model

class Users(Model):
    def __init__(self):
        super().__init__(database = 'users')

# users = Users()

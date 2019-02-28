#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import redis
import config

names = locals()

for key, value in config.redis.items():
    names[key] = redis.Redis(host=value['host'], port=value['port'], db=value['db'])



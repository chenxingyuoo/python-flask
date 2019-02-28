#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import redis

redis_db0 = redis.Redis(host='localhost', port=6379, db=0)
redis_db1 = redis.Redis(host='localhost', port=6379, db=1)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib import request

for i in range(100000):
    with request.urlopen('http://127.0.0.1:5000/') as f:
        data = f.read()
        print('Status:', f.status, f.reason)
        for k, v in f.getheaders():
            print('%s: %s' % (k, v))
        print('Data:', data.decode('utf-8'))
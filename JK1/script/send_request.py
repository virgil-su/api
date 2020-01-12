"""
============================
Author:virgir
Creation_time:2019-12-04
============================
"""
# coding=utf-8

import requests
import json
from script.handle_sign import HandleSign
from script.conf_yaml import Yaml


class Send_requests:
    def __init__(self):
        self.session = requests.session()

    def add_headers(self, data):
        self.session.headers.update(data)
        if 'Authorization' in data:
            self.token = data['Authorization'].split(' ')[-1]

    def send_requests(self, url, method='post', data=None, Json=True, **kwargs):
        data = self.convert_data(data)
        head = Yaml.read_yaml('headers', 'header')['X-Lemonban-Media-Type']
        if hasattr(self, 'token') and head == 'lemonban.v3':
            sig = HandleSign().generate_sign(self.token)
            data.update(sig)
        method = method.lower()
        if method == 'get':
            response = self.session.request(method, url, params=data, **kwargs)
        elif method in ('post', 'patch', 'delete'):
            if Json:
                response = self.session.request(method, url, json=data, **kwargs)
            else:
                response = self.session.request(method, url, data=data, **kwargs)
        else:
            response = '不支持此请求方法'
        return response.json()

    @staticmethod
    def convert_data(data):
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except:
                data = eval(data)
        return data

    def close_session(self):
        self.session.close()

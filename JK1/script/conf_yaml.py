"""
============================
Author:virgir
Creation_time:2019-12-04
============================
"""
# coding=utf-8
import os
from configparser import RawConfigParser

import yaml

from script import PATH


class RW_yaml:
    def __init__(self, filename=None):
        if filename is None:
            self.file = os.path.join(PATH.yaml_path, 'test.yaml')
        else:
            self.file = os.path.join(PATH.yaml_path, filename)

    def read_yaml(self, k, v):
        with open(self.file, encoding='utf8') as f:
            data = yaml.full_load(f)
        return data[k][v]

    @staticmethod
    def write_yaml(file_name, data):
        with open(os.path.join(PATH.yaml_path, file_name), 'w', encoding='utf8')as f:
            yaml.dump(data, f, allow_unicode=True)


Yaml = RW_yaml()


class RW_conf:
    def __init__(self, file_name=None):
        if file_name is None:
            self.file = os.path.join(PATH.conf_path, 'test.conf')
        else:
            self.file = os.path.join(PATH.conf_path, file_name)
        self.conf = RawConfigParser()

    def read_conf(self, k, v):
        self.conf.read(self.file, encoding='utf8')
        data = self.conf[k][v]
        try:
            data = eval(data)
        except Exception:
            pass
        return data

    @staticmethod
    def write_conf(file_name, data):
        conf = RawConfigParser()
        with open(os.path.join(PATH.conf_path, file_name), 'w', encoding='utf8')as f:
            for i in data:
                conf[i] = data[i]
            conf.write(f)


Conf = RW_conf()

if __name__ == '__main__':
    data = {
        "mysql": {
            'port': 3306,
            'host': 'api.lemonban.com',
            'user': 'future',
            'pwd': '123456',
            'db': 'futureloan',
        },
        "headers": {
            'header': {'X-Lemonban-Media-Type': 'lemonban.v2'},
            'url': 'http://api.lemonban.com/futureloan'
        },
        'xlsx': {
            'clunm': 6,
            'clunm1': 8
        }
    }
    Yaml.write_yaml('test.yaml', data)
    Conf.write_conf('test.conf', data)
    print(Conf.read_conf('mysql', 'user'))
    print(Yaml.read_yaml('headers', 'header'))

"""
============================
Author:virgir
Creation_time:2019-12-04
============================
"""
# coding=utf-8
import os, shutil
from script import PATH
from script.mysql import Mysql
from script.send_request import Send_requests
from script.xlsx import Xlsx
from script.parametric import Parametric
from script.conf_yaml import Yaml
import json


class Three_user:
    def __init__(self):
        self.xlsx = Xlsx(file_name='create_user.xlsx', sheet='Sheet1')
        self.data = self.xlsx.read_xlsx()
        self.send_request = Send_requests()
        self.mysql = Mysql()
        self.send_request.add_headers(Yaml.read_yaml('headers', 'header'))

    def close_obj(self):
        self.mysql.close_sql()
        self.send_request.close_session()

    def create_user(self):
        user_info = {}
        for i in self.data:
            data = Parametric.parametric(i.data)
            url = 'http://api.lemonban.com/futureloan' + i.interface
            response = self.send_request.send_requests(url, i.method, data)
            data = json.loads(data)
            user = response['data']
            user.update({'pwd': data['pwd']})
            user_info[i.title] = user
            Yaml.write_yaml('user_info.yaml', user_info)
        self.close_obj()

    @staticmethod
    def del_reports():
        file = os.listdir(PATH.reports_path)
        os.chdir(PATH.reports_path)
        for i in file:
            if os.path.isfile(i):
                os.remove(i)
            else:
                shutil.rmtree(i)


if __name__ == '__main__':
    user = Three_user()
    user.create_user()

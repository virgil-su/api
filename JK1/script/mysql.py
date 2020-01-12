"""
============================
Author:virgir
Creation_time:2019-12-04
============================
"""
# coding=utf-8
import pymysql
import random
from script.conf_yaml import Yaml


class Mysql:
    def __init__(self):
        self.sql = pymysql.connect(host=Yaml.read_yaml('mysql', 'host'),
                                   user=Yaml.read_yaml('mysql', 'user'),
                                   password=Yaml.read_yaml('mysql', 'pwd'),
                                   port=Yaml.read_yaml('mysql', 'port'),
                                   db=Yaml.read_yaml('mysql', 'db'),
                                   charset='utf8',
                                   cursorclass=pymysql.cursors.DictCursor
                                   )
        self.mysql = self.sql.cursor()

    def close_sql(self):
        self.mysql.close()
        self.sql.close()

    def run_sql(self, sql, arg=None, all=True):
        self.mysql.execute(sql, arg)
        self.sql.commit()
        if all:
            return self.mysql.fetchall()
        else:
            return self.mysql.fetchone()

    def create_phone(self):
        while True:
            phone = self.new_phone()
            if self.judge_phone(phone):
                continue
            else:
                break
        return phone

    def judge_phone(self, phone):
        sql = 'select * from member where mobile_phone=%s'
        if self.run_sql(sql, phone):
            return True
        else:
            return False

    @staticmethod
    def new_phone():
        phone_head = random.choice(['135', '189', '157', '186', '131', '189'])
        phone = phone_head + ''.join(random.sample('0123456789', 8))
        return phone


if __name__ == '__main__':
    mysql = Mysql()
    print(mysql.judge_phone('15774630912'))

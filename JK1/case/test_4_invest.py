"""
============================
Author:virgir
Creation_time:2019-12-07
============================
"""
# coding=utf-8

import unittest
from script.xlsx import Xlsx
from script.send_request import Send_requests
from script.mysql import Mysql
from script.parametric import Parametric
from script.conf_yaml import Yaml
from ddt import ddt, data


@ddt
class Test_invest(unittest.TestCase):
    data_xlsx = Xlsx(file_name='test.xlsx', sheet='invest')
    case = data_xlsx.read_xlsx()

    @classmethod
    def setUpClass(cls):
        cls.session = Send_requests()
        cls.mysql = Mysql()
        cls.session.add_headers(Yaml.read_yaml('headers', 'header'))

    @classmethod
    def tearDownClass(cls):
        cls.mysql.close_sql()
        cls.session.close_session()

    @data(*case)
    def test_invest(self, case):
        url = Yaml.read_yaml('headers', 'url') + case.interface
        data = Parametric().parametric(case.data)
        data = self.session.convert_data(data)
        expect = Parametric().parametric(case.expect)
        expect = self.session.convert_data(expect)
        response = self.session.send_requests(url, case.method, data)
        try:
            self.assertEquals(response['code'], expect['code'])
            if case.select_sql:
                sql = Parametric().parametric(case.select_sql)
                user_info = self.mysql.run_sql(sql)
                if case.case_id < 7:
                    if hasattr(Parametric, 'item_id1') is False:
                        setattr(Parametric, 'item_id1', str(user_info[0]['id']))
                    elif hasattr(Parametric, 'item_id2') is False:
                        setattr(Parametric, 'item_id2', str(user_info[0]['id']))
                    elif hasattr(Parametric, 'item_id3') is False:
                        setattr(Parametric, 'item_id3', str(user_info[0]['id']))
                else:
                    amount = float(user_info[0]['amount'])
                    amount = round(amount, 2)
                    self.assertEquals(response['data']['member_id'], user_info[0]['member_id'])
                    self.assertEquals(response['data']['loan_id'], user_info[0]['loan_id'])
                    self.assertEquals(response['data']['is_valid'], user_info[0]['is_valid'])
                    self.assertEquals(response['data']['amount'], amount)
                    self.assertEquals(expect['amount'], amount)
                    self.assertEquals(response['data']['member_id'], expect['member_id'])
                    self.assertEquals(response['data']['loan_id'], int(expect['loan_id']))
                    self.assertEquals(response['data']['amount'], expect['amount'])
                    self.assertEquals(response['data']['is_valid'], expect['is_valid'])

        except AssertionError as e:
            self.data_xlsx.write_xlsx(case.case_id, Yaml.read_yaml('xlsx', 'clunm'), str(response))
            self.data_xlsx.write_xlsx(case.case_id, Yaml.read_yaml('xlsx', 'clunm1'), str(e))
            raise e
        else:
            self.data_xlsx.write_xlsx(case.case_id, Yaml.read_yaml('xlsx', 'clunm'), str(response))
            self.data_xlsx.write_xlsx(case.case_id, Yaml.read_yaml('xlsx', 'clunm1'), '通过')
            if 'token_info' in str(response):
                token = {}
                token['Authorization'] = 'Bearer ' + response['data']['token_info']['token']
                self.session.add_headers(token)

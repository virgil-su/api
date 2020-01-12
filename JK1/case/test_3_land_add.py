"""
============================
Author:virgir
Creation_time:2019-12-06
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
class Test_lan_add(unittest.TestCase):
    data_xlsx = Xlsx(file_name='test.xlsx', sheet='land_add')
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
    def test_lan_add(self, case):
        url = Yaml.read_yaml('headers', 'url') + case.interface
        data = Parametric().parametric(case.data)
        data = self.session.convert_data(data)
        expect = Parametric().parametric(case.expect)
        expect = self.session.convert_data(expect)
        response = self.session.send_requests(url, case.method, data)
        try:
            self.assertEquals(response['code'], expect['code'])
            if case.select_sql:
                user_info = self.mysql.run_sql(case.select_sql, expect['member_id'])
                self.assertEquals(response['data']['member_id'], expect['member_id'])
                self.assertEquals(response['data']['title'], expect['title'])
                self.assertEquals(response['data']['loan_rate'], expect['loan_rate'])
                self.assertEquals(response['data']['loan_term'], expect['loan_term'])
                self.assertEquals(response['data']['loan_date_type'], expect['loan_date_type'])
                self.assertEquals(response['data']['bidding_days'], expect['bidding_days'])
                self.assertEquals(response['data']['amount'], expect['amount'])

                self.assertEquals(response['data']['title'], user_info['title'])
                self.assertEquals(response['data']['loan_rate'], user_info['loan_rate'])
                self.assertEquals(response['data']['loan_term'], user_info['loan_term'])
                self.assertEquals(response['data']['loan_date_type'], user_info['loan_date_type'])
                self.assertEquals(response['data']['bidding_days'], user_info['bidding_days'])
                self.assertEquals(response['data']['amount'], user_info['amount'])
                self.assertEquals(response['data']['id'], user_info['id'])
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

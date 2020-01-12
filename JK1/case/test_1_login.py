"""
============================
Author:virgir
Creation_time:2019-12-05
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
class Test_login(unittest.TestCase):
    data_xlsx = Xlsx(file_name='test.xlsx', sheet='login')
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
    def test_login(self, case):
        url = Yaml.read_yaml('headers', 'url') + case.interface
        data = Parametric().parametric(case.data)
        data = self.session.convert_data(data)
        if case.select_sql:
            user_info = self.mysql.run_sql(case.select_sql, data['mobile_phone'])
            setattr(Parametric, 'login_amount', user_info[0]['leave_amount'])
        response = self.session.send_requests(url, case.method, data)
        expect = Parametric().parametric(case.expect)
        expect = self.session.convert_data(expect)
        try:
            self.assertEquals(response['code'], expect['code'])
            if case.select_sql:
                self.assertEquals(response['data']['id'], expect['id'])
                self.assertEquals(response['data']['reg_name'], expect['reg_name'])
                self.assertEquals(response['data']['mobile_phone'], expect['mobile_phone'])
                self.assertEquals(response['data']['type'], expect['type'])
                self.assertEquals(response['data']['leave_amount'], expect['leave_amount'])
        except AssertionError as e:
            self.data_xlsx.write_xlsx(case.case_id, Yaml.read_yaml('xlsx', 'clunm'), str(response))
            self.data_xlsx.write_xlsx(case.case_id, Yaml.read_yaml('xlsx', 'clunm1'), str(e))
            raise e
        else:
            self.data_xlsx.write_xlsx(case.case_id, Yaml.read_yaml('xlsx', 'clunm'), str(response))
            self.data_xlsx.write_xlsx(case.case_id, Yaml.read_yaml('xlsx', 'clunm1'), '通过')

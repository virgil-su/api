"""
============================
Author:virgir
Creation_time:2019-12-04
============================
"""
# coding=utf-8
import unittest
from ddt import ddt, data
from script.xlsx import Xlsx
from script.send_request import Send_requests
from script.mysql import Mysql
from script.conf_yaml import Yaml
from script.parametric import Parametric


@ddt
class Test_register(unittest.TestCase):
    xlsx_data = Xlsx(file_name='test.xlsx', sheet='register')
    case = xlsx_data.read_xlsx()

    @classmethod
    def setUpClass(cls):
        cls.session = Send_requests()
        cls.session.add_headers(Yaml.read_yaml('headers', 'header'))
        cls.mysql = Mysql()

    @classmethod
    def tearDownClass(cls):
        cls.mysql.close_sql()
        cls.session.close_session()

    @data(*case)
    def test_register(self, case):
        url = Yaml.read_yaml('headers', 'url') + case.interface
        data = Parametric.parametric(case.data)
        response = self.session.send_requests(url, case.method, data)
        if case.select_sql:
            user_info = self.mysql.run_sql(case.select_sql, arg=response['data']['id'])
            setattr(Parametric, 'register_user_name', user_info[0]['reg_name'])
            setattr(Parametric, 'register_user_phone', user_info[0]['mobile_phone'])
        expect = Parametric.parametric(case.expect)
        expect = self.session.convert_data(expect)
        try:
            self.assertEquals(expect['code'], response['code'])
            if case.select_sql:
                self.assertEquals(expect['reg_name'], response['data']['reg_name'])
                self.assertEquals(expect['mobile_phone'], response['data']['mobile_phone'])
        except AssertionError as e:
            self.xlsx_data.write_xlsx(case.case_id, Yaml.read_yaml('xlsx', 'clunm'), str(response))
            self.xlsx_data.write_xlsx(case.case_id, Yaml.read_yaml('xlsx', 'clunm1'), str(e))
            raise e
        else:
            self.xlsx_data.write_xlsx(case.case_id, Yaml.read_yaml('xlsx', 'clunm'), str(response))
            self.xlsx_data.write_xlsx(case.case_id, Yaml.read_yaml('xlsx', 'clunm1'), '通过')

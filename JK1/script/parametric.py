"""
============================
Author:virgir
Creation_time:2019-12-04
============================
"""
# coding=utf-8
import re
from script.mysql import Mysql
from script.conf_yaml import RW_yaml


class Parametric:
    new_user = re.compile(r'\${new_user}')
    register_reg_name = re.compile(r'\${register_reg_name}')
    register_mobile_phone = re.compile(r'\${register_mobile_phone}')
    loan_name = re.compile(r'\${loan_name}')
    invest_name = re.compile(r'\${invest_name}')
    admin_name = re.compile(r'\${admin_name}')
    loan_pwd = re.compile(r'\${loan_pwd}')
    invest_pwd = re.compile(r'\${invest_pwd}')
    admin_pwd = re.compile(r'\${admin_pwd}')
    invest_phone = re.compile(r'\${invest_user}')
    admin_phone = re.compile(r'\${admin_user}')
    loan_phone = re.compile(r'\${loan_user}')
    login_leave_amount = re.compile(r'\${login_amount}')
    invest_id = re.compile(r'\${invest_id}')
    admin_id = re.compile(r'\${admin_id}')
    loan_id = re.compile(r'\${loan_id}')
    not_id = re.compile(r'\${not_id}')
    new_loan_phone = re.compile(r'\${new_loan_user}')
    new_loan_id = re.compile(r'\${new_loan_id}')
    new_loan_pwd = re.compile(r'\${new_loan_pwd}')
    invest_item_id1 = re.compile(r'\${item_id1}')
    invest_item_id2 = re.compile(r'\${item_id2}')
    invest_item_id3 = re.compile(r'\${item_id3}')

    @classmethod
    def parametric(cls, data):
        if data is None:
            return data
        mysql = Mysql()
        Yaml = RW_yaml('user_info.yaml')
        if re.search(cls.new_user, data):
            new_phone = mysql.create_phone()
            data = re.sub(cls.new_user, new_phone, data)
        if re.search(cls.register_mobile_phone, data):
            user_name = getattr(Parametric, 'register_user_phone')
            data = re.sub(cls.register_mobile_phone, user_name, data)
        if re.search(cls.register_reg_name, data):
            user_phone = getattr(Parametric, 'register_user_name')
            data = re.sub(cls.register_reg_name, user_phone, data)
        if re.search(cls.loan_name, data):
            data = re.sub(cls.loan_name, Yaml.read_yaml('loan_user', 'reg_name'), data)
        if re.search(cls.invest_name, data):
            data = re.sub(cls.invest_name, Yaml.read_yaml('invest_user', 'reg_name'), data)
        if re.search(cls.admin_name, data):
            data = re.sub(cls.admin_name, Yaml.read_yaml('admin_user', 'reg_name'), data)
        if re.search(cls.admin_phone, data):
            data = re.sub(cls.admin_phone, Yaml.read_yaml('admin_user', 'mobile_phone'), data)
        if re.search(cls.invest_phone, data):
            data = re.sub(cls.invest_phone, Yaml.read_yaml('invest_user', 'mobile_phone'), data)
        if re.search(cls.loan_phone, data):
            data = re.sub(cls.loan_phone, Yaml.read_yaml('loan_user', 'mobile_phone'), data)
        if re.search(cls.invest_pwd, data):
            data = re.sub(cls.invest_pwd, Yaml.read_yaml('invest_user', 'pwd'), data)
        if re.search(cls.loan_pwd, data):
            data = re.sub(cls.loan_pwd, Yaml.read_yaml('loan_user', 'pwd'), data)
        if re.search(cls.admin_pwd, data):
            data = re.sub(cls.admin_pwd, Yaml.read_yaml('admin_user', 'pwd'), data)
        if re.search(cls.login_leave_amount, data):
            login_amount = getattr(Parametric, 'login_amount')
            data = re.sub(cls.login_leave_amount, str(login_amount), data)
        if re.search(cls.admin_id, data):
            data = re.sub(cls.admin_id, str(Yaml.read_yaml('admin_user', 'id')), data)
        if re.search(cls.loan_id, data):
            data = re.sub(cls.loan_id, str(Yaml.read_yaml('loan_user', 'id')), data)
        if re.search(cls.invest_id, data):
            data = re.sub(cls.invest_id, str(Yaml.read_yaml('invest_user', 'id')), data)
        if re.search(cls.not_id, data):
            sql = 'select max(id) from member'
            not_id = mysql.run_sql(sql)
            not_id = str(not_id[0]['max(id)'] + 1)
            data = re.sub(cls.not_id, not_id, data)
        if re.search(cls.new_loan_id, data):
            data = re.sub(cls.new_loan_id, str(Yaml.read_yaml('new_loan_user', 'id')), data)
        if re.search(cls.new_loan_pwd, data):
            data = re.sub(cls.new_loan_pwd, str(Yaml.read_yaml('new_loan_user', 'pwd')), data)
        if re.search(cls.new_loan_phone, data):
            data = re.sub(cls.new_loan_phone, str(Yaml.read_yaml('new_loan_user', 'mobile_phone')), data)
        if re.search(cls.invest_item_id1, data):
            item_id1 = getattr(Parametric, 'item_id1')
            data = re.sub(cls.invest_item_id1, item_id1, data)
        if re.search(cls.invest_item_id2, data):
            item_id2 = getattr(Parametric, 'item_id2')
            data = re.sub(cls.invest_item_id2, item_id2, data)
        if re.search(cls.invest_item_id3, data):
            item_id3 = getattr(Parametric, 'item_id3')
            data = re.sub(cls.invest_item_id3, item_id3, data)

        mysql.close_sql()
        return data


if __name__ == '__main__':
    P = Parametric()
    data = P.parametric('{"mobile_phone": "${new_user}","pwd": "12345678","type": null,"reg_name": "借款人"}')
    print(data)

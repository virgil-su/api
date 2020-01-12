"""
============================
Author:virgir
Creation_time:2019-12-04
============================
"""
# coding=utf-8

import os
# 绝对路径
Path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 用例路径
xlsx_path = os.path.join(Path, 'datas')
# 配置文件路径
yaml_path = os.path.join(Path, 'configs')
conf_path = os.path.join(Path, 'configs')
# 测试报告路径
reports_path = os.path.join(Path, 'reports')
# 测试用例类路径
case_path = os.path.join(Path, 'case')
# 日志文件路径
log_path = os.path.join(Path, 'log')

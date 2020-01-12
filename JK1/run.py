"""
============================
Author:virgir
Creation_time:2019-12-05
============================
"""
# coding=utf-8

import os
from unittest import TestLoader, TestSuite
from script import PATH
from script import create_user
# from case import test_4_invest
from HTMLTestRunnerNew import HTMLTestRunner
import datetime


class Run:
    def __init__(self, file_name=None):
        if file_name is None:
            self.filename = 'test'
        else:
            self.filename = file_name
        if os.path.exists(os.path.join(PATH.conf_path, 'user_info.yaml')):
            pass
        else:
            create_user.Three_user().create_user()

    def run_test(self):
        suit = TestSuite()
        load = TestLoader()
        # suit.addTest(load.loadTestsFromModule(test_4_invest))
        suit.addTest(load.discover(PATH.case_path))
        self.filename = self.filename + '_' + str(datetime.datetime.now().strftime('%Y%m%d%H%M%S')) + '.html'
        create_user.Three_user().del_reports()
        with open(os.path.join(PATH.reports_path, self.filename), 'wb')as f:
            runs = HTMLTestRunner(stream=f,
                                  verbosity=2,
                                  title='测试报告',
                                  description='内容',
                                  tester='virgil')
            runs.run(suit)



run = Run()
run.run_test()

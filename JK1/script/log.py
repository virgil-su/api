"""
============================
Author:virgir
Creation_time:2019-12-04
============================
"""
# coding=utf-8
from script.PATH import log_path
import logging
import os


class Log:
    @classmethod
    def log(cls, log_name=None, file_name=None):
        if log_name is None:
            log_name = 'virgil'
        if file_name is None:
            file_name = 'test.log'
        str_format = '%(asctime)s - [%(filename)s-->line:%(lineno)d] - %(name)s:%(levelname)s: %(message)s'
        output_format = logging.Formatter(str_format)
        log = logging.getLogger(log_name)
        log.setLevel('DEBUG')
        log_output = logging.StreamHandler()
        log_output.setLevel('INFO')
        log_output.setFormatter(output_format)
        log.addHandler(log_output)
        log_output_file = logging.FileHandler(os.path.join(log_path, file_name), 'w', encoding='utf8')
        log_output_file.setLevel('ERROR')
        log_output_file.setFormatter(output_format)
        log.addHandler(log_output_file)
        return log


log = Log().log()

if __name__ == '__main__':
    log.info('asdf')
    log.error('大沙发打发士大夫')

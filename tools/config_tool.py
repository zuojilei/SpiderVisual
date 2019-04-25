#!/bin/python
# coding:utf8

import configparser
import threading


class ConfigTool(object):
    '''配置文件管理类'''
    instance = None
    _instance_lock = threading.Lock()

    def getFile(self):
        return 'config/env.ini'

    def __new__(cls, *args, **kwargs):
        """单例模块"""
        if not hasattr(ConfigTool, "_instance"):
            cls.config = configparser.ConfigParser()
            cls.config.read('../config/env.ini', encoding='utf8')
            with ConfigTool._instance_lock:
                if not hasattr(ConfigTool, "_instance"):
                    ConfigTool._instance = object.__new__(cls, *args, **kwargs)
        return ConfigTool._instance

    def get(self, section, option):
        """
        获取配置文件
        :param section:
        :param option:
        :return:
        """
        return self.config.get(section, option)

    def items(self, section):
        '''
        读取section下所有配置
        :param section:
        :return:
        '''
        return self.config.items(section)

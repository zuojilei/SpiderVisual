#!/usr/bin/python
# coding:utf-8

import pymysql
from tools.clean_log import CleanLog
from tools.config_tool import ConfigTool
from DBUtils.PooledDB import PooledDB
import threading


class Connect(object):
    """mysql数据库基类"""
    __pool = None
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        """单例模块"""
        if not hasattr(Connect, "_instance"):
            cls.__instance()
            with Connect._instance_lock:
                if not hasattr(Connect, "_instance"):
                    Connect._instance = object.__new__(cls, *args, **kwargs)
        return Connect._instance

    def __init__(self):
        pass

    # mysql连接
    @classmethod
    def __instance(cls):
        MYSQL_HOSTS = ConfigTool().get('mysql', 'mysql_host')
        MYSQL_PORT = ConfigTool().get('mysql', 'mysql_port')
        MYSQL_USER = ConfigTool().get('mysql', 'mysql_user')
        MYSQL_PASSWORD = ConfigTool().get('mysql', 'mysql_pass')
        MYSQL_CHAR = ConfigTool().get('mysql', 'mysql_char')
        MYSQL_DB = ConfigTool().get('mysql', 'mysql_db')


        if Connect.__pool is None:
            cls.__pool = PooledDB(creator=pymysql, mincached=1, maxcached=20,
                                  host=MYSQL_HOSTS, port=int(MYSQL_PORT), user=MYSQL_USER, passwd=MYSQL_PASSWORD,
                                  db=MYSQL_DB, use_unicode=False, charset=MYSQL_CHAR,
                                  cursorclass=pymysql.cursors.DictCursor)
        cls.con = cls.__pool.connection()
        cls.cur = cls.con.cursor()

    # mysql 中断后重新连接
    def again_conn(self):
        try:
            self.con.ping()
        except Exception as e:
            Connect.__instance()

    # 得到连接conn
    def get_conn(self):
        self.again_conn()
        return self.con

    # 得到游标
    def get_cur(self):
        self.again_conn()
        return self.cur

    # 关闭数据库连接
    def close(self):
        self.con.close()

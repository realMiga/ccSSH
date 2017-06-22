#!/usr/bin/env python
# encoding: utf-8

from Core.BaseDB import BaseDB


class ShadowManager:
    dbConn = BaseDB()
    tabel = 't_server_list'

    def __init__(self):
        pass

    @staticmethod
    def get_all_server():
        sql = '''SELECT * FROM t_server_list'''
        return ShadowManager.dbConn.select(sql)


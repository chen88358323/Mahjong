# -*- coding:utf-8 -*-
# 作者：NoamaNelson
# 日期：2021/11/19
# 文件名称：conf.py
# 作用：configparser模块的使用
# 联系：VX(NoamaNelson)
# 博客：https://blog.csdn.net/NoamaNelson

import configparser
import os


class Conf:
    def __init__(self):
        self.conf = configparser.ConfigParser()
        self.root_path = os.path.dirname(os.path.abspath(__file__))
        self.f = os.path.join(self.root_path + "/config.conf")
        self.conf.read(self.f)

    def read_sections(self):
        print(f"1、获取所有的sections:{self.conf.sections()}")

    def read_options(self, s1, s2):
        print(f"2、获取mysqldb所有的options:{self.conf.options(s1)}")
        print(f"3、获取mailinfo所有的options:{self.conf.options(s2)}")

    def read_conf(self, m, n):
        name = self.conf.get(m, n)  # 获取指定section的option值
        name =str(name)
        return name
        # print(f"4、获取指定section:{m}下的option：{n}的值为{name}")
    def readDbConf(self,name):
        val=self.conf.get('mysqldb',name)
        # print("key "+name +" val  "+val)
        return  val
    def readEsConf(self,name):
        val=self.conf.get('elasticsearch',name)
        # print("key "+name +" val  "+val)
        return  val


    def get_items(self, m, n):
        print(f"5、获取sectoion:{m}下的配置信息为：{self.conf.items(m)}")
        print(f"6、获取sectoion:{n}下的配置信息为：{self.conf.items(n)}")

    def set_option(self, m, n, s):
        self.conf.set(m, n, s)
        self.conf.write(open(self.f, "w"))
        print(f"7、设置setion:{m}下的option:{n}的值为：{s}")

    def has_s_o(self, s, o):
        print(f"8、检查section：{s}是否存在：{self.conf.has_section(s)}")
        print(f"9、检查section：{s}下的option：{o}是否存在：{self.conf.has_option(s, o)}")

    def add_s_o(self, s, o, v):
        if not self.conf.has_section(s):
            self.conf.add_section(s)
            print(f"10、添加新的section为{s}")
        else:
            print(f"10、添加新的section为{s}已经存在，无需添加！")
        if not self.conf.has_option(s, o):
            self.conf.set(s, o, v)
            print(f"11、要添加的option为{o}, 值为{v}")
        else:
            print(f"11、要添加的option为{o}, 值为{v}，已经存在，无需添加！")
        self.conf.write(open(self.f, "w"))

    def remove_s_o(self, s, o):
        if self.conf.has_section(s):
            self.conf.remove_section(s)
            print(f"12、删除section:{s}==OK!")
        else:
            print(f"12、要删除的section:{s}不存在，不用删除！")
        if self.conf.has_option(s, o):
            self.conf.remove_option(s, o)
            print(f"13、删除section：{s}下的option：{o}==OK!")
        else:
            print(f"13、要删除的section：{s}下的option：{o}不存在，不用删除！")


if __name__ == "__main__":
    aa = Conf()
    aa.read_sections()
    aa.read_options("mysqldb", "mailinfo")
    aa.read_conf("mysqldb", "db_host")
    aa.get_items("mysqldb", "mailinfo")
    aa.readDbConf("db_host")
    # aa.set_option("mysqldb", "sql_name", "游客")
    # aa.has_s_o("mysqldb", "sql_name")
    # aa.add_s_o("login", "name", "root")
    # aa.remove_s_o("login", "name")

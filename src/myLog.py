# encoding: utf-8
'''
@author: season
@contact: shiter@live.cn

@file: myLog.py
@time: 2019/3/7 16:27
@desc:
屏幕加日志输出：https://www.cnblogs.com/nancyzhu/p/8551506.html
多模块调用：https://www.cnblogs.com/zhuque/p/8320925.html
'''

import sys
import os

import logging


CURRENT_URL = os.path.dirname(__file__)
PARENT_URL = os.path.abspath(os.path.join(CURRENT_URL, os.pardir))
sys.path.append(PARENT_URL)
#
# logging.basicConfig(                                                                #通过具体的参数来更改logging模块默认行为；
#     level=logging.DEBUG,                                                            #设置告警级别为ERROR；
#     format="%(asctime)s---%(lineno)s----%(name)s: %(message)s",                     #自定义打印的格式；
#     filename="spider_log.txt",                                                      #将日志输出到指定的文件中；
#     filemode="a",                                                                   #以追加的方式将日志写入文件中，w是以覆盖写的方式哟;
# )

import logging
from logging import handlers

class Logger(object):
    level_relations = {
        'debug':logging.DEBUG,
        'info':logging.INFO,
        'warning':logging.WARNING,
        'error':logging.ERROR,
        'crit':logging.CRITICAL
    }#日志级别关系映射

    def __init__(self,filename,level='info',when='D',backCount=3,fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'):
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt)#设置日志格式
        self.logger.setLevel(self.level_relations.get(level))#设置日志级别
        sh = logging.StreamHandler()#往屏幕上输出
        sh.setFormatter(format_str) #设置屏幕上显示的格式
        th = handlers.TimedRotatingFileHandler(filename=filename,when=when,backupCount=backCount,encoding='utf-8')#往文件里写入#指定间隔时间自动生成文件的处理器
        #实例化TimedRotatingFileHandler
        #interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒
        # M 分
        # H 小时、
        # D 天、
        # W 每星期（interval==0时代表星期一）
        # midnight 每天凌晨
        th.setFormatter(format_str)#设置文件里写入的格式
        self.logger.addHandler(sh) #把对象加到logger里
        self.logger.addHandler(th)

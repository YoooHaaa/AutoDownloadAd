# !/usr/bin/env python3
# -*-coding:utf-8 -*-

import colorlog
import logging
import os

class Log:
    log_colors = {
        'DEBUG': 'white',  
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    } 
    log_level = {
        'debug':logging.DEBUG,
        'info':logging.INFO,
        'warning':logging.WARNING,
        'error':logging.ERROR,
        'crit':logging.CRITICAL
    }
    log_info:logging.Logger = None
    log_debug:logging.Logger = None
    log_error:logging.Logger = None


    @classmethod
    def init(cls):
        cls.log_info = cls.init_console_file("info")
        cls.log_debug = cls.init_file("debug")
        cls.log_error = cls.init_console_file('error')
        

    @classmethod
    def init_console_file(cls, level) -> logging.Logger:
        try:
            log_obj = logging.getLogger(level)   # 获取一个logger对象
            log_obj.setLevel(cls.log_level[level])             # 设置日志输出等级
            # 创建一个文件的handler
            file_handler = logging.FileHandler("./log/" + level + '.log')
            file_handler.setLevel(cls.log_level[level])
            # 创建一个控制台的handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(cls.log_level[level])
            # 设置格式化
            if False:
                f_fmt='[%(asctime)s.%(msecs)03d] -> %(levelname)s : %(message)s'
                c_fmt='%(log_color)s[%(asctime)s.%(msecs)03d] -> %(levelname)07s : %(message)s'
            else:
                f_fmt='[%(asctime)s.%(msecs)03d] %(filename)s -> %(funcName)s line:%(lineno)d [%(levelname)s] : %(message)s'
                c_fmt='%(log_color)s[%(asctime)s.%(msecs)03d] %(filename)s -> %(funcName)s line:%(lineno)d [%(levelname)s] : %(message)s'
            # 设置日志的输出格式
            file_fmt = logging.Formatter(
                f_fmt,
                datefmt='%Y-%m-%d  %H:%M:%S'
            ) 
            console_fmt = colorlog.ColoredFormatter(
                c_fmt,
                datefmt='%Y-%m-%d  %H:%M:%S',
                log_colors=cls.log_colors
            )
            # 给handler绑定一个fomatter类
            file_handler.setFormatter(file_fmt)
            console_handler.setFormatter(console_fmt)
            # 绑定handler
            log_obj.addHandler(file_handler)
            log_obj.addHandler(console_handler)
            return log_obj
        except Exception as err:
            print("error in Log -> init_console_file:" + str(err))
        return None



    @classmethod
    def init_file(cls, level) -> logging.Logger:
        try:
            log_obj = logging.getLogger(level)   
            log_obj.setLevel(cls.log_level[level])  
            # 创建一个文件的handler
            file_handler = logging.FileHandler("./log/" + level + '.log')
            file_handler.setLevel(cls.log_level[level])
            # 设置格式化
            f_fmt='[%(asctime)s.%(msecs)03d] %(filename)s -> %(funcName)s line:%(lineno)d [%(levelname)s] : %(message)s'
            # 设置日志的输出格式
            file_fmt = logging.Formatter(
                f_fmt,
                datefmt='%Y-%m-%d  %H:%M:%S'
            ) 
            # 给handler绑定一个fomatter类
            file_handler.setFormatter(file_fmt)
            # 绑定handler
            log_obj.addHandler(file_handler)
            return log_obj
        except Exception as err:
            print("error in Log -> init_file:" + str(err))
        return None



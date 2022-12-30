# !/usr/bin/env python3
# -*-coding:utf-8 -*-

import abc

class BaseParse(metaclass=abc.ABCMeta):
    dump:dict = {} 

    def __init__(self):
        pass

    @abc.abstractmethod
    def parse(self, flow:str):
        pass


    @abc.abstractmethod
    def parse_video(self,info):
        pass


    @abc.abstractmethod
    def parse_web(self,info):
        pass






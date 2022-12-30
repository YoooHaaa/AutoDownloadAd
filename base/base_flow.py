# !/usr/bin/env python3
# -*-coding:utf-8 -*-


import abc
import threading


class BaseFlow(threading.Thread, metaclass=abc.ABCMeta):
    def __init__(self):
        threading.Thread.__init__(self)
        self.m_switch = True


    @abc.abstractmethod
    def catch(self):
        pass


    def run(self):
        self.catch()


    def stop(self):
        self.m_switch = False

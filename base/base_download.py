# !/usr/bin/env python3
# -*-coding:utf-8 -*-


import threading
import abc


class BaseDownload(threading.Thread, metaclass=abc.ABCMeta):
    def __init__(self):
        threading.Thread.__init__(self)
        self.m_switch = True


    @abc.abstractmethod
    def download(self):
        pass


    def run(self):
        self.download()


    def stop(self):
        self.m_switch = False




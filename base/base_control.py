# !/usr/bin/env python3
# -*-coding:utf-8 -*-


import threading
import abc


class BaseControl(threading.Thread, metaclass=abc.ABCMeta):
    def __init__(self, refresh:int, interval:int):
        threading.Thread.__init__(self)
        self.m_switch = True
        self.refresh = refresh
        self.interval = interval

    @abc.abstractmethod
    def into_model(self):
        pass

    @abc.abstractmethod
    def loop(self):
        pass

    def run(self):
        if self.into_model():
            self.loop()


    def stop(self):
        self.m_switch = False




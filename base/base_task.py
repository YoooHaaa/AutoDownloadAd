# !/usr/bin/env python3
# -*-coding:utf-8 -*-

import abc
from utils.log import Log
from base.base_model import BaseModel


class BaseTask(metaclass=abc.ABCMeta):

    def __init__(self, refresh:int, interval:int):
        self.refresh = refresh
        self.interval = interval
        self.task:BaseModel = None


    def run(self):
        try:
            self.create_task()
            self.task.start()
        except Exception as err:
            Log.log_error.error(str(err))


    @abc.abstractmethod
    def create_task(self):
        pass






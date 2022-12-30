# !/usr/bin/env python3
# -*-coding:utf-8 -*-

from utils.log import Log
from base.base_task import BaseTask
from model.search.search_model import SearchModel

class SearchTask(BaseTask):

    def __init__(self, refresh:int, interval:int, keyword:str):
        BaseTask.__init__(self, refresh, interval)
        self.keyword = keyword


    def create_task(self):
        self.task = SearchModel(self.refresh, self.interval, self.keyword)


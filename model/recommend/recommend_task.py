# !/usr/bin/env python3
# -*-coding:utf-8 -*-


from base.base_task import BaseTask
from model.recommend.recommend_model import RecommendModel

class RecommendTask(BaseTask):

    def __init__(self, refresh:int, interval:int):
        BaseTask.__init__(self, refresh, interval)


    def create_task(self):
        self.task = RecommendModel(self.refresh, self.interval)


# !/usr/bin/env python3
# -*-coding:utf-8 -*-

from data.env import GlobalEnv
import uiautomator2 as u2
from config.config import Config
from queue import Queue
import random
from model.search.search_task import SearchTask
from model.recommend.recommend_task import RecommendTask
from base.base_task import BaseTask


class TaskPool(object):

    def __init__(self):
        GlobalEnv.global_device = u2.connect_usb(Config.config_device_id)
        GlobalEnv.update_window_size()
        self.task:Queue[BaseTask] = Queue(maxsize=0)
        self.init_task()


    def init_task(self):
        if Config.config_model == 1:
            self.get_search_task()
        elif Config.config_model == 2:
            self.get_recommend_task()
        elif Config.config_model == 3:
            self.get_mix_task()


    def get_search_task(self):
        print("搜索模式")
        list_words = []
        for i in range(Config.config_search_cycle):
            random.shuffle(Config.config_search_words)
            list_words += Config.config_search_words
        for keyword in list_words:
            self.task.put(SearchTask(Config.config_search_refresh, Config.config_search_interval, keyword))


    def get_recommend_task(self):
        print("推荐模式")
        self.task.put(RecommendTask(Config.config_recommend_refresh, Config.config_recommend_interval))


    def get_mix_task(self):
        print("混合模式")
        list_words = []
        for i in range(Config.config_search_cycle):
            random.shuffle(Config.config_search_words)
            list_words += Config.config_search_words
        for i, keyword in enumerate(list_words):
            if i != 0 and i % Config.config_mix_limit == 0:
                self.task.put(RecommendTask(Config.config_recommend_refresh, Config.config_recommend_interval))
            self.task.put(SearchTask(Config.config_search_refresh, Config.config_search_interval, keyword))


    def excute(self):
        while True:
            if self.task.empty():
                return
            else:
                self.task.get().run()


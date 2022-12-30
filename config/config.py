# !/usr/bin/env python3
# -*-coding:utf-8 -*-

import json

class Config:
    config_packagename = ''
    config_device_id = ""
    config_model = 0
    config_search_cycle = 0
    config_search_refresh = 0
    config_search_interval = 0
    config_search_words = None
    config_recommend_refresh = 0
    config_recommend_interval = 0
    
    @classmethod
    def init(cls):
        try:
            with open("config/config.json", "r", encoding="utf-8") as f:
                config = json.load(f)
                cls.config_device_id = config["deviceid"]
                cls.config_packagename = config["packagename"]
                cls.config_model = config["model"]
                cls.config_search_words:list = config["search"]["keywords"]
                cls.config_search_cycle = config["search"]["cycle"]
                cls.config_search_like = config["search"]["like"]
                cls.config_search_refresh = config["search"]["refresh"]
                cls.config_search_interval = config["search"]["interval"]
                cls.config_recommend_refresh = config["recommend"]["refresh"]
                cls.config_recommend_like = config["recommend"]["like"]
                cls.config_recommend_interval = config["recommend"]["interval"]
                cls.config_mix_limit = config["mix"]["search_limit"]
                cls.config_exit = config["exit"]
        except Exception as e:
            print(str(e))






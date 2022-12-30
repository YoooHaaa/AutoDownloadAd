# !/usr/bin/env python3
# -*-coding:utf-8 -*-

from utils.log import Log
from data.env import GlobalEnv
import copy
import datetime
import os
from base.base_parse import BaseParse

class RecommendParse(BaseParse):
    dump:dict = {} 

    def __init__(self):
        BaseParse.__init__(self)
        self.filename = ''


    def parse(self, flow:str):
        try:
            flow = flow.strip().replace("\r\n", "")
            GlobalEnv.update_file_path()
            if flow.find("<web>") != -1:
                info = flow.split("douyin  : ")[1]
                self.parse_web(info.split("<web>")[1])
            elif flow.find("<recommend-video>") != -1:
                info = flow.split("douyin  : ")[1]
                self.parse_video(info.split("<recommend-video>")[1])
            elif flow.find("<web-all>") != -1:
                Log.log_debug.debug(flow)
        except Exception as err:
            Log.log_error.error(str(err))



    def parse_video(self,info):
        try:
            GlobalEnv.update_video(info)
        except Exception as err:
            Log.log_error.error(str(err))



    def parse_web(self, info:str):
        try:
            Log.log_info.info(info)
            infos = info.split(",")
            self.filename = str(datetime.datetime.now())[0:19].replace(" ", "-").replace(":", "-")
            GlobalEnv.set_recommend_current_download(open=True, web_title=infos[0], web_url=infos[1], web_download=infos[2], filename=self.filename)
        except Exception as err:
            Log.log_error.error(str(err))








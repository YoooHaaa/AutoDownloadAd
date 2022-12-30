# !/usr/bin/env python3
# -*-coding:utf-8 -*-

from utils.log import Log
from data.env import GlobalEnv
import copy
import datetime
import os
from base.base_parse import BaseParse

class SearchParse(BaseParse):
    dump:dict = {} 

    def __init__(self):
        BaseParse.__init__(self)


    def parse(self, flow:str):
        try:
            if not GlobalEnv.global_search_parse_switch:
                return
            flow = flow.strip().replace("\r\n", "")
            GlobalEnv.update_file_path()
            if flow.find("<web>") != -1:
                info = flow.split("douyin  : ")[1]
                self.parse_web(info.split("<web>")[1])
            elif flow.find("<search-video>") != -1:
                info = flow.split("douyin  : ")[1]
                self.parse_video(info.split("<search-video>")[1])
            elif flow.find("<web-all>") != -1:
                Log.log_debug.debug(flow)
        except Exception as err:
            Log.log_error.error(str(err))



    def parse_video(self,info):
        try:
            if GlobalEnv.get_ad_status():
                GlobalEnv.set_ad_status(False)
                if self.dump:
                    self.dump["video_url"] = info
                    filename = str(datetime.datetime.now())[0:19].replace(" ", "-").replace(":", "-")
                    self.dump["filename"] = filename
                    self.create_dir(self.dump["web_title"])
                    GlobalEnv.set_search_queue_download(copy.deepcopy(self.dump))
                    GlobalEnv.set_search_screenshot_state(copy.deepcopy([True, self.dump["web_title"], filename]))
                    self.dump = {}
        except Exception as err:
            Log.log_error.error(str(err))



    def parse_web(self,info):
        try:
            infos = info.split(",")
            self.dump["web_title"] = infos[0]
            self.dump["web_url"] = infos[1]
            self.dump["web_download"] = infos[2]
            GlobalEnv.set_ad_status(True)
        except Exception as err:
            Log.log_error.error(str(err))



    def create_dir(self, dirname):
        try:
            if not os.path.exists(GlobalEnv.global_file_path + '/search/' + dirname):
                os.mkdir(GlobalEnv.global_file_path + '/search/' + dirname)
        except:
            pass




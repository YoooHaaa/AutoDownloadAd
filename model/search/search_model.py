# !/usr/bin/env python3
# -*-coding:utf-8 -*-

from utils.log import Log
from data.env import GlobalEnv
from base.base_model import BaseModel
from runtime.event import EventType, EventRuntime
from model.search.search_parse import SearchParse
from model.search.search_flow import SearchModelFlow
from model.search.search_control import SearchControl
from model.search.search_download import SearchDownload
from utils.log import Log
import time
import os


class ParseNotFoundException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class SearchModel(BaseModel):

    def __init__(self, refresh:int, interval:int, keyword:str):
        BaseModel.__init__(self, "search")
        GlobalEnv.global_search_parse_switch = False
        self.refresh = refresh
        self.interval = interval
        self.keyword = keyword
        

    def start(self):
        try:
            if not GlobalEnv.global_thread_douyin:
                return
            self.register()
            while True:
                if not GlobalEnv.global_thread_douyin:
                    Log.log_info.info("程序正在关闭......")
                    self.stop()
                    return
                if self.m_control.isAlive():
                    time.sleep(1)
                else:
                    self.stop()
                    return
        except Exception as err:
            Log.log_error.error(str(err))


    def stop(self):
        '''
        退出模式任务
        '''
        self.m_flow_catch.stop()
        self.m_control.stop()
        self.m_download.stop()
        self.un_reg_runtime()
        self.wait_download()


    def wait_download(self):
        while True:
            if GlobalEnv.get_thread_list_alive():
                Log.log_info.info("等待下载线程执行完......")
                time.sleep(5)
            else:
                return


    def reg_flow(self): 
        try:
            if self.m_flow_parse:
                if not self.m_flow_catch or not self.m_flow_catch.isAlive():
                    self.m_flow_catch = SearchModelFlow(self.m_flow_parse.parse, "douyin")
                    self.m_flow_catch.setDaemon(True)
                    self.m_flow_catch.start()
            else:
                raise ParseNotFoundException('搜索模式流量解析类未注册')
        except Exception as err:
            Log.log_error.error(str(err))


    def reg_parse(self):
        try:
            if not self.m_flow_parse:
                self.m_flow_parse = SearchParse()
        except Exception as err:
            Log.log_error.error(str(err))


    def reg_screen_control(self):
        try:
            self.m_control = SearchControl(self.refresh, self.interval, self.keyword)
            self.m_control.setDaemon(True)
            self.m_control.start()
        except Exception as err:
            Log.log_error.error(str(err))


    def reg_download(self):
        try:
            if not self.m_download or not self.m_download.isAlive():
                self.m_download = SearchDownload()
                self.m_download.setDaemon(True)
                self.m_download.start()
        except Exception as err:
            Log.log_error.error(str(err))


    # def create_dir(self):
    #     try:
    #         if not os.path.exists(GlobalEnv.global_file_path + '/recommend'):
    #             os.mkdir(GlobalEnv.global_file_path + '/recommend')
    #     except:
    #         pass


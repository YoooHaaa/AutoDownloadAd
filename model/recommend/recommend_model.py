# !/usr/bin/env python3
# -*-coding:utf-8 -*-

from utils.log import Log
from data.env import GlobalEnv
from base.base_model import BaseModel
from model.recommend.recommend_parse import RecommendParse
from model.recommend.recommend_flow import RecommendModelFlow
from model.recommend.recommend_control import RecommendControl
from model.recommend.recommend_download import RecommendDownload
from utils.log import Log
import time
from utils.uiauto import UiAuto
import os

class ParseNotFoundException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class RecommendModel(BaseModel):

    def __init__(self, refresh:int, interval:int, ):
        BaseModel.__init__(self, "recommend")
        self.refresh = refresh
        self.interval = interval
        
        
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
        UiAuto.release_watch()
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
        if self.m_flow_parse:
            if not self.m_flow_catch or not self.m_flow_catch.isAlive():
                self.m_flow_catch = RecommendModelFlow(self.m_flow_parse.parse, "douyin")
                self.m_flow_catch.setDaemon(True)
                self.m_flow_catch.start()
        else:
            raise ParseNotFoundException('搜索模式流量解析类未注册')


    def reg_parse(self):
        if not self.m_flow_parse:
            self.m_flow_parse = RecommendParse()


    def reg_screen_control(self):
        self.m_control = RecommendControl(self.refresh, self.interval)
        self.m_control.setDaemon(True)
        self.m_control.start()


    def reg_download(self):
        if not self.m_download or not self.m_download.isAlive():
            self.m_download = RecommendDownload()
            self.m_download.setDaemon(True)
            self.m_download.start()







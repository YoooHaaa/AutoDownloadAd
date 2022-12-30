# !/usr/bin/env python3
# -*-coding:utf-8 -*-

from data.env import GlobalEnv
import time
from base.base_control import BaseControl
from utils.uiauto import UiAuto
from utils.log import Log
import datetime
import random
from runtime.event import EventType, EventRuntime
import copy
from config.config import Config
import os

class RecommendControl(BaseControl):
    def __init__(self, refresh:int, interval:int):
        BaseControl.__init__(self, refresh, interval)
        UiAuto.device_monitor_dlg()
        self.count_time = 0
        Log.log_info.info('推荐模式 屏控 线程开启...')


    def loop(self):
        try:
            while True:
                try:
                    if not self.m_switch:
                        UiAuto.release_watch()
                        return
                    Log.log_info.info('in RecommendControl run time->' + str(datetime.datetime.now())[0:19] + "  total->" + str(self.count_time) + "\n")
                    if self.count_time > Config.config_recommend_refresh or not UiAuto.check_top():
                        self.m_switch = False   
                        Log.log_info.info('推荐模式 屏控 线程正在结束...')
                        UiAuto.release_watch()
                        return
                    self.count_time += 1
                    self.start_swipe()
                except Exception as err:
                    self.m_switch = False
                    Log.log_error.error(str(err))
        except Exception as err:
            self.m_switch = False
            UiAuto.release_watch()
            Log.log_error.error(str(err))


    def into_model(self) -> bool:
        try:
            UiAuto.light_screen()
            UiAuto.device_start_app()
            time.sleep(10)
        except Exception as err:
            Log.log_error.error(str(err))
            return False
        return True


    def start_swipe(self):
        try:
            current = GlobalEnv.get_recommend_current_download()
            UiAuto.device_swipe_random()
            if current and current['open']:
                time.sleep(1)
                if current['web_title'] != '':
                    if UiAuto.device_loop_check_ad(current['web_title']):
                        self.create_dir(current['web_title'])
                        EventRuntime().on_event(EventType.FUNC_DOWNLOAD_PNG, filename=GlobalEnv.global_file_path + "/recommend/" + current['web_title'] + "/" + current['filename'] + ".png")
                        if Config.config_recommend_like:
                            UiAuto.device_point_like_and_focus() #未登录账号时不能点赞
                        download = {"video_url":GlobalEnv.get_video_previous(), 
                                    "web_title":current['web_title'], 
                                    "web_url":current['web_url'], 
                                    "web_download":current['web_download'], 
                                    "filename":current['filename']}
                        GlobalEnv.set_recommend_queue_download(copy.deepcopy(download))
                        GlobalEnv.set_recommend_current_download(open=False)
            time.sleep(random.randint(Config.config_recommend_interval, Config.config_recommend_interval + 3))
        except Exception as err:
            Log.log_error.error(str(err))
            

    def create_dir(self, dirname):
        try:
            if not os.path.exists(GlobalEnv.global_file_path + '/recommend/' + dirname):
                os.mkdir(GlobalEnv.global_file_path + '/recommend/' + dirname)
        except:
            pass
            



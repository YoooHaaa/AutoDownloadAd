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
from config.config import Config

class SearchControl(BaseControl):
    def __init__(self, refresh:int, interval:int, keyword:str):
        BaseControl.__init__(self, refresh, interval)
        self.keyword = keyword
        UiAuto.device_monitor_dlg()
        self.count_time = 0
        Log.log_info.info('搜索模式 屏控 线程开启...')

    def loop(self):
        try:
            while True:
                try:
                    if not self.m_switch:
                        UiAuto.release_watch()
                        return
                    Log.log_info.info('in SearchControl run time->' + str(datetime.datetime.now())[0:19] + "  total->" + str(self.count_time) + "\n")
                    if self.count_time > self.refresh or not UiAuto.check_top():
                        self.m_switch = False   
                        Log.log_info.info('搜索模式 屏控 线程正在结束...')
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
            time.sleep(5)
            UiAuto.device_click(0.928, 0.063)  # 搜索图标 
            time.sleep(2)
            UiAuto.device_click(0.322, 0.067)  # 搜索光标
            time.sleep(2)
            Log.log_info.info("输入关键词 -> " + self.keyword)
            UiAuto.device_input(self.keyword)  # 输入搜索词
            time.sleep(2)
            UiAuto.device_click(0.922, 0.064)  # 搜索按钮
            time.sleep(2)
            UiAuto.device_swipe_down()         # 下拉刷新
            time.sleep(10)
            self.find_and_click_video()        # 点击搜索结果视频
            GlobalEnv.global_search_parse_switch = True #此时才能进行搜索的流量解析
            time.sleep(3)
        except Exception as err:
            Log.log_error.error(str(err))
            return False
        return True


    def find_and_click_video(self):
        if UiAuto.device_xpath_word_exists('@com.ss.android.ugc.aweme:id/tv_desc'):
            x,y = UiAuto.device_get_xpath_center('@com.ss.android.ugc.aweme:id/tv_desc')
            if y + 300 < GlobalEnv.global_window_height:
                Log.log_info.info("找到元素 tv_desc -> x=" + str(x) + " y=" + str(y))
                UiAuto.device_click(x, y + 250)
            else:
                UiAuto.device_swipe_up()
                self.find_and_click_video()
        else:
            UiAuto.device_swipe_up()
            self.find_and_click_video()


    def start_swipe(self):
        try:
            status, title, name = GlobalEnv.get_search_screenshot_state()
            GlobalEnv.set_search_screenshot_state([False, "", ""])
            UiAuto.device_swipe_random()
            if status:
                time.sleep(1)
                EventRuntime().on_event(EventType.FUNC_DOWNLOAD_PNG, filename=GlobalEnv.global_file_path + "/search/" + title + "/" + name + ".png")
                if Config.config_search_like:
                    UiAuto.device_point_like_and_focus() #未登录账号时不能点赞
                time.sleep(random.randint(3, 5))
            time.sleep(random.randint(self.interval, self.interval + 3))
        except Exception as err:
            Log.log_error.error(str(err))
            




            



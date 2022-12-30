# !/usr/bin/env python3
# -*-coding:utf-8 -*-

import threading
from uiautomator2 import Device
import os
import sys
from queue import Queue
import datetime
import threading
from typing import List
import copy
from config.config import Config
'''
Queue:         FIFO（先入先出)队列
LifoQueue:     LIFO（后入先出）队列
PriorityQueue: 优先级队列
'''

class GlobalEnv:

    global_thread_lock = None
    global_thread_douyin = True
    global_thread_list:List[threading.Thread] = list()
    global_file_path = ""
    global_window_width = 0
    global_window_height = 0
    global_device:Device = None
    global_search_queue_download:Queue = None     
    global_search_is_screenshot:list = []
    global_recommend_current_download:dict = {}
    global_recommend_queue_download:Queue = None
    global_ad_status = False
    global_video_previous = ''
    global_video_current = ''
    global_search_parse_switch = False

    @classmethod
    def init(cls):
        cls.global_thread_lock = threading.Lock()  # 同步锁
        cls.global_path = os.path.dirname(os.path.abspath(sys.argv[0]))
        cls.global_search_queue_download = Queue(maxsize=0)    # 0为无限大
        cls.global_recommend_queue_download = Queue(maxsize=0)    # 0为无限大
        cls.global_search_is_screenshot = [False, "", ""]
        cls.global_file_path = 'out/' + str(datetime.datetime.now())[0:10]
        Config.init()
        cls.init_dir()
        cls.init_thread_list()


    @classmethod
    def init_dir(cls):
        try:
            if not os.path.exists('log'):
                os.mkdir('log')
            if not os.path.exists('out'):
                os.mkdir('out')
            if not os.path.exists(cls.global_file_path):
                os.mkdir(cls.global_file_path)
        except:
            pass


    @classmethod
    def update_window_size(cls):
        cls.global_window_width, cls.global_window_height = cls.global_device.window_size()


    @classmethod
    def update_file_path(cls):
        cls.global_file_path = 'out/' + str(datetime.datetime.now())[0:10]
        try:
            if not os.path.exists(cls.global_file_path):
                os.mkdir(cls.global_file_path)
        except:
            pass


    # @classmethod
    # def update_keyword(cls):
    #     if cls.global_keyword == "":
    #         random.shuffle(Config.config_search_words) # 随机打乱
    #         cls.global_keyword = Config.config_search_words[0]
    #     else:
    #         key_len = len(Config.config_search_words)
    #         for i, key in enumerate(Config.config_search_words):
    #             if cls.global_keyword == key:
    #                 if i == key_len - 1:
    #                     random.shuffle(Config.config_search_words)
    #                     cls.global_keyword = Config.config_search_words[0]
    #                 else:
    #                     cls.global_keyword = Config.config_search_words[i + 1]
    #                 break



    @classmethod
    def init_thread_list(cls):
        cls.global_thread_lock.acquire()
        cls.global_thread_list:List[threading.Thread] = list()
        cls.global_thread_lock.release()    
    @classmethod
    def update_thread_list(cls, th:threading.Thread):
        cls.global_thread_lock.acquire()
        for thr in cls.global_thread_list:
            if not thr.isAlive():
                cls.global_thread_list.remove(thr)
        cls.global_thread_list.append(th)
        cls.global_thread_lock.release()
    @classmethod
    def get_thread_list_alive(cls) -> bool:
        cls.global_thread_lock.acquire()
        ret = False
        for thr in cls.global_thread_list:
            if thr.isAlive():
                ret = True
        cls.global_thread_lock.release()
        return ret


    @classmethod
    def get_search_screenshot_state(cls):
        '''
        [False, "title", "name"]
        '''
        cls.global_thread_lock.acquire()
        status = cls.global_search_is_screenshot
        cls.global_thread_lock.release()
        return status
    @classmethod
    def set_search_screenshot_state(cls, status):
        '''
        [False, "title", "name"]
        '''
        cls.global_thread_lock.acquire()
        cls.global_search_is_screenshot = status
        cls.global_thread_lock.release()


    @classmethod
    def set_search_queue_download(cls, info:dict): 
        '''
        {web_title, web_url, web_download, video_url, filename}
        '''
        cls.global_thread_lock.acquire()
        cls.global_search_queue_download.put(info)
        cls.global_thread_lock.release() 
    @classmethod
    def get_search_queue_download(cls):
        '''
        {web_title, web_url, web_download, video_url, filename}
        '''
        cls.global_thread_lock.acquire()
        if cls.global_search_queue_download.empty():
            info = None
        else:
            info = cls.global_search_queue_download.get()
        cls.global_thread_lock.release()
        return info


    @classmethod
    def set_recommend_queue_download(cls, info:dict): 
        '''
        {video_url, web_title, web_url, web_download, filename}
        '''
        cls.global_thread_lock.acquire()
        cls.global_recommend_queue_download.put(info)
        cls.global_thread_lock.release() 
    @classmethod
    def get_recommend_queue_download(cls):
        '''
        {video_url, web_title, web_url, web_download, filename}
        '''
        cls.global_thread_lock.acquire()
        if cls.global_recommend_queue_download.empty():
            info = None
        else:
            info = cls.global_recommend_queue_download.get()
        cls.global_thread_lock.release()
        return info


    @classmethod
    def set_recommend_current_download(cls, open=False, web_title='', web_url='', web_download='', filename=''):
        with cls.global_thread_lock:
            cls.global_recommend_current_download["open"] = open
            cls.global_recommend_current_download["web_title"] = web_title
            cls.global_recommend_current_download["web_url"] = web_url
            cls.global_recommend_current_download["web_download"] = web_download
            cls.global_recommend_current_download["filename"] = filename
    @classmethod
    def get_recommend_current_download(cls) -> dict:
        download = None
        with cls.global_thread_lock:
            download = copy.deepcopy(cls.global_recommend_current_download)
        return download



    @classmethod
    def get_ad_status(cls):
        cls.global_thread_lock.acquire()
        status = cls.global_ad_status
        cls.global_thread_lock.release() 
        return status
    @classmethod
    def set_ad_status(cls, status):
        cls.global_thread_lock.acquire()
        cls.global_ad_status = status
        cls.global_thread_lock.release() 


    @classmethod
    def get_video_previous(cls) -> str:
        video = ''
        with cls.global_thread_lock:
            video = cls.global_video_previous
        return video
    @classmethod
    def get_video_current(cls) -> str:
        video = ''
        with cls.global_thread_lock:
            video = cls.global_video_current
        return video
    @classmethod
    def update_video(cls, video):
        with cls.global_thread_lock:
            cls.global_video_previous = cls.global_video_current
            cls.global_video_current = video







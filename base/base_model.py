# !/usr/bin/env python3
# -*-coding:utf-8 -*-


import abc
from utils.log import Log
from data.env import GlobalEnv
from runtime.event import EventType, EventRuntime
import requests
import datetime
from utils.screenshot import ScreenShot
import threading
import os



class BaseModel(metaclass=abc.ABCMeta):
    def __init__(self, name:str):
        self.m_model_name = name
        self.m_flow_parse = None
        self.m_flow_catch = None
        self.m_control = None
        self.m_download = None
        self.create_dir()


    @abc.abstractmethod
    def start(self):
        pass

    @abc.abstractmethod
    def reg_flow(self):
        pass

    @abc.abstractmethod
    def reg_parse(self):
        pass

    @abc.abstractmethod
    def reg_screen_control(self):
        pass

    @abc.abstractmethod
    def reg_download(self):
        pass

    def register(self):
        try:
            self.reg_runtime()
            self.reg_parse()
            self.reg_flow()
            self.reg_screen_control()
            self.reg_download()
        except Exception as err:
            Log.log_error.error(str(err))


    def reg_runtime(self):
        EventRuntime().reg_event(EventType.FUNC_DOWNLOAD_APK, self._callback_download_apk)
        EventRuntime().reg_event(EventType.FUNC_DOWNLOAD_PNG, self._callback_download_png)
        EventRuntime().reg_event(EventType.FUNC_DOWNLOAD_VIDEO, self._callback_download_video)
        EventRuntime().reg_event(EventType.FUNC_DUMP_INFO, self._callback_dump_info)


    def un_reg_runtime(self):
        EventRuntime().unreg_event(EventType.FUNC_DOWNLOAD_APK, self._callback_download_apk)
        EventRuntime().unreg_event(EventType.FUNC_DOWNLOAD_PNG, self._callback_download_png)
        EventRuntime().unreg_event(EventType.FUNC_DOWNLOAD_VIDEO, self._callback_download_video)
        EventRuntime().unreg_event(EventType.FUNC_DUMP_INFO, self._callback_dump_info)


    def _callback_dump_info(self, event_type, **kwargs):
        '''
        kwargs: download, web, title, video
        '''
        file_list = [GlobalEnv.global_file_path + '/' + self.m_model_name + '/' + kwargs['title'] + '/' + kwargs['title'] + '.txt', 
                    GlobalEnv.global_file_path + '/' + self.m_model_name + '/out.txt']
        for filename in file_list:
            try:
                with open(filename, "a", encoding='utf-8') as log:
                    log.write(str(datetime.datetime.now())[0:19])
                    log.write("\n")
                    log.write(kwargs['title'])
                    log.write("\n")
                    log.write("APK下载链接:" + kwargs['download'])
                    log.write("\n")
                    log.write("广告链接:" + kwargs['web'])
                    log.write("\n")
                    log.write("视频链接:" + kwargs['video'])
                    log.write("\n")
                    log.write("\n")
            except Exception as err:
                Log.log_error.error(str(err))


    def _callback_download_png(self, event_type, **kwargs):
        '''
        kwargs: filename
        '''
        try:
            ScreenShot.dump_screen(kwargs['filename'])
        except Exception as err:
            Log.log_error.error(str(err))


    def _callback_download_apk(self, event_type, **kwargs):
        '''
        kwargs: url, dirname, filename
        '''
        def thread_download_apk(url, filename):
            try:
                if os.path.exists(filename):
                    return
                res = requests.get(url) # 下载超过5分钟则停止下载  timeout=(9.05, 300)
                if(res.status_code == 404):
                    Log.log_error.error(filename + ' 下载失败:' + url)
                    return
                with open(filename, "wb") as apk:
                    apk.write(res.content)
            except Exception as err:
                Log.log_error.error(str(err))
        th = threading.Thread(target=thread_download_apk, args=(kwargs['url'], kwargs['dirname'] + '/' + kwargs['filename']))
        th.start()
        GlobalEnv.update_thread_list(th)


    def _callback_download_video(self, event_type, **kwargs):
        '''
        kwargs: url, dirname, filename
        '''
        def thread_download_video(url, filename):
            try:
                if os.path.exists(filename):
                    return
                response = requests.get(url, stream=True)
                if(response.status_code == 404):
                    Log.log_error.error(filename + ' 下载失败:' + url)
                    return
                with open(filename, 'ab') as f:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)  
            except Exception as err:
                Log.log_error.error(str(err))
        th = threading.Thread(target=thread_download_video, args=(kwargs['url'], kwargs['dirname'] + '/' + kwargs['filename']))
        th.start()
        GlobalEnv.update_thread_list(th)


    def create_dir(self):
        try:
            if not os.path.exists(GlobalEnv.global_file_path + '/' + self.m_model_name):
                os.mkdir(GlobalEnv.global_file_path + '/' + self.m_model_name)
        except:
            pass

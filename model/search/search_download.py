# !/usr/bin/env python3
# -*-coding:utf-8 -*-

from data.env import GlobalEnv
import time
from utils.log import Log
from runtime.event import EventType, EventRuntime
from base.base_download import BaseDownload

class SearchDownload(BaseDownload):
    def __init__(self):
        BaseDownload.__init__(self)
        Log.log_info.info('搜索模式 下载 线程开启...')


    def download(self):
        try:
            while True:
                if not self.m_switch:
                    Log.log_info.info('搜索模式 下载 线程正在结束...')
                    return
                time.sleep(1)
                self._download()
        except Exception as err:
            self.m_switch = False
            Log.log_error.error(str(err))



    def _download(self):
        try:
            download = GlobalEnv.get_search_queue_download()
            if download:
                Log.log_info.info("get ad -> " + str(download))
                if download['web_download']:
                    EventRuntime().on_event(EventType.FUNC_DOWNLOAD_APK, url=download['web_download'], 
                                            dirname=GlobalEnv.global_file_path + '/search/' + download['web_title'], 
                                            filename=download['filename'] + '.apk')
                if download['video_url']:
                    EventRuntime().on_event(EventType.FUNC_DOWNLOAD_VIDEO, url=download['video_url'], 
                                            dirname=GlobalEnv.global_file_path + '/search/' + download['web_title'], 
                                            filename=download['filename'] + '.mp4')
                if download['web_url']:
                    EventRuntime().on_event(EventType.FUNC_DUMP_INFO, download=download['web_download'], 
                                            web=download['web_url'], 
                                            title=download['web_title'], 
                                            video=download['video_url'])
        except Exception as err:
            Log.log_error.error(str(err))




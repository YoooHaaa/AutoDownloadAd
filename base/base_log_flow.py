# !/usr/bin/env python3
# -*-coding:utf-8 -*-



import os
import time
from utils.log import Log
import subprocess
from base.base_flow import BaseFlow
from config.config import Config

class LogFlow(BaseFlow):
    def __init__(self, callback, tag):
        BaseFlow.__init__(self)
        self.m_parse_callback = callback
        self.m_tag = tag
        
        
    def clear_log(self):
        '''
        function: 清理日志缓存并重新设置日志缓存大小
        '''
        try:
            os.system('adb -s ' + Config.config_device_id + ' logcat -c')
            os.system('adb -s ' + Config.config_device_id + ' logcat -G 200m')
        except Exception as err:
            Log.log_error.error(str(err))


    def catch(self):
        '''
        function: 不间断读取用户层日志
        '''
        try:
            self.clear_log()
            while True:
                try:
                    if not self.m_switch:
                        Log.log_info.info('Log接受 线程正在结束...')
                        return
                    obj = subprocess.Popen('adb -s ' + Config.config_device_id + ' logcat -s ' + self.m_tag, shell = True, stdin=subprocess.PIPE, stdout=subprocess.PIPE ,stderr=subprocess.PIPE)
                    for item in iter(obj.stdout.readline, 'b'):
                        if not self.m_switch:
                            Log.log_info.info('LogFlow over...')
                            return
                        self.m_parse_callback(str(item.decode('utf-8')))
                except Exception as err:
                    Log.log_error.error(str(err))   
                time.sleep(3)     
        except Exception as err:
            self.m_switch = False
            Log.log_error.error(str(err))






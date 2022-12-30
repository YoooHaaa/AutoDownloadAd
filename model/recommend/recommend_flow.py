# !/usr/bin/env python3
# -*-coding:utf-8 -*-



from utils.log import Log
from base.base_log_flow import LogFlow

class RecommendModelFlow(LogFlow):

    def __init__(self, parse, tag):
        LogFlow.__init__(self, parse, tag)
        Log.log_info.info('推荐模式 logcat 线程开启...')

        
        







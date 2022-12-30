# !/usr/bin/env python3
# -*-coding:utf-8 -*-


import time
from utils.log import Log
import os
from utils.uiauto import UiAuto

class ScreenShot():


    @classmethod
    def dump_screen(cls, filename):
        try:
            if os.path.exists(filename):
                return
            UiAuto.device_screenshot(filename)
            time.sleep(0.1)
        except Exception as err:
            Log.log_error.error(str(err))



        
        




# !/usr/bin/env python3
# -*-coding:utf-8 -*-

import keyboard
from data.env import GlobalEnv
from config.config import Config

class HotKey(object):
    def __init__(self):
        super(HotKey, self).__init__()
        self.reg_hotkey()


    def reg_hotkey(self):
        keyboard.add_hotkey(Config.config_exit, self._exit)



    def _exit(self):
        GlobalEnv.global_thread_douyin = False










# !/usr/bin/env python3
# -*-coding:utf-8 -*-

from data.env import GlobalEnv
from utils.log import Log
from task.task_pool import TaskPool
from utils.hotkey import HotKey

if __name__ == "__main__":
    GlobalEnv.init() 
    Log.init()
    HotKey()
    TaskPool().excute()








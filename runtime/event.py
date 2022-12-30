#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import threading
from typing import Dict, Set, Callable
from base.base_singleton import SingletonType
from enum import Enum


class EventType(Enum):
    FUNC_DOWNLOAD_PNG = 1
    FUNC_DOWNLOAD_VIDEO = 2
    FUNC_DOWNLOAD_APK = 3
    FUNC_DUMP_INFO = 4


class EventRuntime(metaclass=SingletonType):
    def __init__(self):
        self.m_events_data = {}  
        self.m_callbacks: Dict[EventType, Set[Callable]] = {}
        self.m_lock = threading.Lock()
        self.__init_m_callbacks()


    def __init_m_callbacks(self):
        for event_type in EventType:
            self.m_callbacks[event_type] = set()


    def on_event(self, event_type, **kwargs):
        with self.m_lock:
            self.m_events_data[event_type] = kwargs
            if event_type in self.m_callbacks:
                for callback_func in self.m_callbacks[event_type]:
                    callback_func(event_type, **kwargs)


    def reg_event(self, event_type, callback):
        '''
        callback: cb(event_type, **kwargs)
        '''
        with self.m_lock:
            self.m_callbacks[event_type].add(callback)


    def unreg_event(self, event_type:EventType, callback:Callable):
        with self.m_lock:
            if event_type not in self.m_callbacks:
                return
            self.m_callbacks[event_type].discard(callback)




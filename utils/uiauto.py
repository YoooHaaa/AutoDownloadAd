# !/usr/bin/env python3
# -*-coding:utf-8 -*-


from utils.log import Log
from data.env import GlobalEnv
import random
import os
import time
from config.config import Config

class UiAuto():
    ctx = None

    def __init__(cls):
        pass

    @classmethod
    def device_monitor_dlg(cls):
        try:
            cls.release_watch()
            cls.ctx = GlobalEnv.global_device.watch_context()
            cls.ctx.when("取消").click()
            cls.ctx.when("退出").click()
            cls.ctx.when("下次再说").click()
            cls.ctx.when("以后再说").click()
            cls.ctx.when("我知道了").click()
            cls.ctx.when("拒绝").click()
            cls.ctx.wait_stable() 
        except Exception as err:
            Log.log_error.error(str(err))

    @classmethod
    def release_watch(cls):
        try:
            cls.ctx.stop()
        except:
            pass

    @classmethod
    def device_input(cls, info):
        GlobalEnv.global_device.send_keys(info)

    @classmethod
    def device_click(cls, x, y):
        GlobalEnv.global_device.click(x, y)

    @classmethod
    def device_xpath_click(cls, id):
        try:
            GlobalEnv.global_device.xpath(id).get().click()
        except:
            pass   


    @classmethod
    def device_start_app(cls):
        try:
            #GlobalEnv.global_device.app_start(GlobalEnv.global_packagename, stop=True) 抖音无法用此方法启动
            cls.device_stop_app()
            time.sleep(1)
            os.system('adb -s ' + Config.config_device_id + ' shell am start -n com.ss.android.ugc.aweme/.splash.SplashActivity')
        except Exception as err:
            Log.log_error.error(str(err))

    @classmethod
    def device_stop_app(cls):
        try:
            GlobalEnv.global_device.app_stop(Config.config_packagename)
        except Exception as err:
            pass

    @classmethod
    def device_swipe_random(cls):
        try:
            print('正在滑屏... ...')
            xbase = random.random()
            xtop = random.random()
            x1 = (xbase / 2.5) + 0.3
            y1 = (xbase / 10) + 0.7
            x2 = (xtop / 2.5) + 0.3
            y2 = (xtop / 10) + 0.2
            step = xbase / 10 + 0.2
            GlobalEnv.global_device.swipe(x1, y1, x2, y2, step)
        except Exception as err:
            Log.log_error.error(str(err))

    @classmethod
    def device_swipe_up(cls):
        try:
            GlobalEnv.global_device.swipe_ext('up', 1)
        except Exception as err:
            Log.log_error.error(str(err))

    @classmethod
    def device_swipe_down(cls):
        try:
            GlobalEnv.global_device.swipe_ext('down', 1)
        except Exception as err:
            Log.log_error.error(str(err))

    @classmethod
    def device_home(cls):
        try:
            GlobalEnv.global_device.press("home")
        except Exception as err:
            Log.log_error.error(str(err))


    @classmethod
    def device_screen_state(cls) -> bool:
        try:
            state = GlobalEnv.global_device.info.get('screenOn')
        except Exception as err:
            Log.log_error.error(str(err))
            return False
        return state


    @classmethod
    def device_back(cls):
        try:
            GlobalEnv.global_device.press("back")
        except Exception as err:
            Log.log_error.error(str(err))

    @classmethod
    def device_stop_app(cls):
        try:
            GlobalEnv.global_device.app_stop(Config.config_packagename)
        except Exception as err:
            Log.log_error.error(str(err))

    @classmethod
    def device_xpath_word_exists(cls, word) -> bool:
        '''
        检查当前页面是否存在指定词
        '''
        try:
            ret = GlobalEnv.global_device.xpath(word).exists
            return ret
        except Exception as err:
            Log.log_error.error(str(err))
        return False

    @classmethod
    def device_get_xpath_center(cls, id):
        try:
            x,y = GlobalEnv.global_device.xpath(id).get().center()
        except Exception as err:
            Log.log_error.error(str(err))
        return x,y      


    @classmethod
    def device_current(cls) -> dict:
        '''
        获取当前顶层应用信息
        '''
        try:
            cur = GlobalEnv.global_device.app_current()
        except Exception as err:
            Log.log_error.error(str(err))
        return cur

    @classmethod
    def device_point_like_and_focus(cls):
        '''
        点赞或关注或收藏
        '''
        try:
            x,y = GlobalEnv.global_device.xpath('@com.ss.android.ugc.aweme:id/user_avatar').get().center()
            # GlobalEnv.global_device.click(x/GlobalEnv.global_window_width, y/GlobalEnv.global_window_height + 0.025)  # 关注
            if random.randint(0, 1):
                try:
                    GlobalEnv.global_device.click(x/GlobalEnv.global_window_width, y/GlobalEnv.global_window_height + 0.0746) # 点赞
                except:
                    pass   
            if random.randint(0, 1):
                try:
                    GlobalEnv.global_device.click(x/GlobalEnv.global_window_width, y/GlobalEnv.global_window_height + 0.2354) # 收藏
                except:
                    pass    
        except Exception as err:
            Log.log_error.error(str(err))


    @classmethod
    def device_screen_on(cls):
        try:
            GlobalEnv.global_device.screen_on()
        except Exception as err:
            Log.log_error.error(str(err))

    @classmethod
    def device_screen_off(cls):
        try:
            GlobalEnv.global_device.screen_off()
        except Exception as err:
            Log.log_error.error(str(err))

    @classmethod
    def device_check_screen(cls) -> bool:
        '''
        检查是否黑屏
        '''
        try:
            ret = True
            ret = GlobalEnv.global_device.xpath('@').exists
        except Exception as err:
            ret = False
            Log.log_error.error(str(err))
        return ret


    @classmethod
    def device_screenshot(cls, path):
        GlobalEnv.global_device.screenshot(path)

    @classmethod
    def reboot(cls):
        os.system('adb reboot')

    @classmethod
    def device_loop_check_ad(cls, title) -> bool:
        if cls.device_xpath_word_exists(title):
            return True
        else:
            time.sleep(2)
            if cls.device_xpath_word_exists(title):
                return True
            else:
                time.sleep(2)
                if cls.device_xpath_word_exists(title):
                    return True
        return False

    @classmethod
    def light_screen(cls):
        if not cls.device_screen_state():
            cls.device_screen_on()
            time.sleep(2)
            cls.device_swipe_up()
            time.sleep(2)
        
    @classmethod
    def check_top(cls):
        '''
        True: APP, False:非APP或黑屏
        '''
        try:
            if not cls.device_check_screen():
                return False
            current = cls.device_current()
            if current['package'] != Config.config_packagename:
                time.sleep(10)
                return True
        except Exception as err:
            Log.log_error.error(str(err))
        return True
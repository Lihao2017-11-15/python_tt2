# -*- coding: UTF-8 -*-
from ctypes import *  # 获取屏幕上某个坐标的颜色
from random import *
from inc.FormAPI import *
from inc.kmAPI import *
import autopy
import pyautogui as auto
from inc.change_keyboard_layout import *

if __name__ == "__main__":
    win_title = "GitHub Login"
    while True:
        form = FormControl()
        form.bindWindowByName(None, win_title)
        form.WindowActive()
        time.sleep(1)
        if form is not None:
            if form.getWinTitle() != win_title:
                continue
            else:
                change_keyboard(Lan.EN) # 切换为英文输入法
                auto.typewrite("812256@qq.com")
                auto.press('tab')
                auto.typewrite("password")
                auto.press('enter')

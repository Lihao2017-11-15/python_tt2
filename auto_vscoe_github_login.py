# -*- coding: UTF-8 -*-
from ctypes import *  # 获取屏幕上某个坐标的颜色
from random import *
from inc.FormAPI import *
from inc.kmAPI import *
import autopy
import pyautogui as auto

if __name__ == "__main__":
    win_title = "GitHub Login"
    form = FormControl()
    form.bindWindowByName(None, win_title)
    form.WindowActive()
    time.sleep(0.5)

    while True:
        form.bindActiveWindow()
        time.sleep(1)
        if form is not None:
            if form.getWinTitle() != win_title:
                continue
            else:
                auto.press('shift')
                auto.typewrite("812256@qq.com")
                auto.press('tab')
                auto.typewrite("password")
                auto.press('enter')

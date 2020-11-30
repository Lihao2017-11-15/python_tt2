# -*- coding: UTF-8 -*-
from ctypes import *  # 获取屏幕上某个坐标的颜色
from random import *
from inc.FormAPI import *
from inc.kmAPI import *
import win32api,win32gui,win32con #导入win32api相关模块
import autopy
import pyautogui as auto  



if __name__ == "__main__":
    # win_title = "GitHub Login"
    win_title = "Notepad"
    form = FormControl()
    form.bindWindowByName(None, win_title)
    form.WindowActive()
    time.sleep(0.5)

    while True:
        form.bindActiveWindow()
        time.sleep(1)
        if form is not None:
            if form.getWinTitle() != "Lineage II":
                continue
            else:
                auto.typewrite("812256@qq.com")
                auto.press('tab')
                auto.typewrite("password")
                auto.press('enter')

from ctypes import * 
from random import *
from inc.FormAPI import *
from inc.kmAPI import *
import autopy
import pyautogui as auto
from inc.change_keyboard_layout import *


def auto_login(username, password):
    win_title = "GitHub Login"
    while True:
        form = FormControl()
        form.bindWindowByName(None, win_title)
        form.WindowActive()
        time.sleep(0.5)
        if form is not None:
            if form.getWinTitle() != win_title:
                continue
            else:
                try:
                    windll.user32.BlockInput(1) # 禁用鼠标键盘
                    change_keyboard(Lan.EN)  # 切换为英文输入法
                    auto.typewrite(username)
                    auto.press('tab')
                    auto.typewrite(password)
                    auto.press('enter')
                    change_keyboard(Lan.ZH)
                finally:
                    windll.user32.BlockInput(0) # 启用鼠标键盘


#参数类使用实例
if __name__ == "__main__":
    # https://docs.python.org/zh-cn/dev/library/argparse.html
    print("在管理员权限下运行才可以禁止键盘鼠标干扰")
    import argparse
    parser = argparse.ArgumentParser(description='VS插件GitHub自动登录')
    parser.add_argument('-u', '--username', default="812256@qq.com", help="帐号")
    parser.add_argument('-p', '--password', default="", help='密码', required=True)
    args = parser.parse_args()
    print(args)
    print("程序运行中...")

    auto_login(args.username, args.password)

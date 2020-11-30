import win32api, win32gui, win32con
from enum import Enum


class Lan(Enum):
    """
    语言代码值参考：https://msdn.microsoft.com/en-us/library/cc233982.aspx
    """
    EN = 0x4090409
    ZH = 0x8040804


def change_keyboard(lan: Lan):
    """
    修改当前激活窗口输入法
    :param lan: 语言类型
    :return: True 修改成功，False 修改失败
    """
    # 获取系统输入法列表
    hwnd = win32gui.GetForegroundWindow()
    im_list = win32api.GetKeyboardLayoutList()
    im_list = list(map(hex, im_list))

    # 加载输入法
    if hex(lan.value) not in im_list:
        win32api.LoadKeyboardLayout('0000' + hex(lan.value)[-4:], 1)

    result = win32api.SendMessage(hwnd, win32con.WM_INPUTLANGCHANGEREQUEST, 0,
                                  lan.value)
    if result == 0:
        print('设置%s键盘成功！' % lan.name)
    return result == 0


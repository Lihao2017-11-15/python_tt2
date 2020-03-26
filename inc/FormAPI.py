import win32con
import win32api
import win32gui
import win32ui
from ctypes import *
from ctypes import wintypes

GetForegroundWindow = windll.user32.GetForegroundWindow
GetWindowRect = windll.user32.GetWindowRect
SetForegroundWindow = windll.user32.SetForegroundWindow
GetWindowText = windll.user32.GetWindowTextA
MoveWindow = windll.user32.MoveWindow
EnumWindows = windll.user32.EnumWindows


class RECT(Structure):
    _fields_ = [
        ('left', c_long),
        ('top', c_long),
        ('right', c_long),
        ('bottom', c_long)
    ]


class POINT(Structure):
    _fields_ = [
        ('x', c_long),
        ('y', c_long),
    ]


class FormControl(object):
    def __init__(self):
        self.win_hd = None
        self.win_title = ''

    def bindActiveWindow(self):
        """
        函数功能：获取当前焦点所在窗口
        """
        self.win_hd = GetForegroundWindow()

    def bindWindowByName(self, class_name, title_name):
        """
        函数功能：根据窗体名获取窗体句柄
        """
        # self.win_title = win_name
        # pro_fun_type = CFUNCTYPE(c_bool, c_int, c_long)
        # pro_fun_p = pro_fun_type(self.EnumWindowsProc)
        # EnumWindows(pro_fun_p, None)
        self.win_hd = win32gui.FindWindow(class_name, title_name)

    def getWinRect(self):
        """
        函数功能：获取窗体的位置和大小
        """
        if self.win_hd is None:
            return None
        rect = RECT()
        GetWindowRect(self.win_hd, byref(rect))
        return rect

    def toScreenPos(self, x, y):
        """
        函数功能：将窗体内部坐标转换为相对于显示屏的绝对坐标
        """
        # 未指定窗口，则结束函数
        if self.win_hd is None:
            return None
        rect = self.getWinRect()
        # 指定的坐标不在窗体内，则结束函数
        if x < 0 or y < 0 or x > rect.right or y > rect.bottom:
            return None
        pos = POINT()
        pos.x = x + rect.left
        pos.y = y + rect.top
        return pos

    def toWindowPos(self, x, y):
        """
        函数功能：将绝对坐标转换成相对于窗体内部坐标
        """
        if self.win_hd is None:
            return None
        rect = self.getWinRect()
        pos = POINT()
        pos.x = x - rect.left
        pos.y = y - rect.top
        # 指定的坐标不在窗体内，则结束函数
        if pos.x < 0 or pos.y < 0 or pos.x > rect.right or pos.y > rect.bottom:
            return None
        return pos

    def WindowActive(self):
        """
        函数功能：将窗体置前
        """
        if self.win_hd is None:
            return None
        SetForegroundWindow(self.win_hd)

    def getHWND(self):
        return self.win_hd

    def getWinTitle(self):
        """
        函数功能：获取窗体的标题
        """
        if self.win_hd is None:
            return None
        buffer = create_string_buffer(255, '\0')
        GetWindowText(self.win_hd, buffer, 255)
        value = buffer.value.decode('gbk')
        return value

    def MoveTo(self, x, y):
        """
        函数功能：移动窗体到指定坐标位置
        """
        if self.win_hd is None:
            return None
        rect = self.getWinRect()
        MoveWindow(self.win_hd, x, y, rect.right -
                   rect.left, rect.bottom-rect.top, True)

    def WinCapture(self, path, x, y, w, h):
        """
        函数功能：抓取窗体截图，并保存到文件
        参    数：path 保存路径
                 x 截取起始x坐标（窗体内相对坐标）
                 y 截取起始y坐标（窗体内相对坐标）
                 w 截取宽度,为0则取窗体宽度
                 h 截取长度,为0则取窗体高度
        """
        if self.win_hd is None:
            return None
        rect = self.getWinRect()
        if w == 0:
            w = rect.right - rect.left
        if h == 0:
            h = rect.bottom - rect.top
        if x < 0 or y < 0 or (x+w) > rect.right or (y+h) > rect.bottom:
            return None
        self.Capture(self.win_hd, path, x, y, w, h, 0)

    def WinCapture_Mem(self, x, y, w, h):
        """
        函数功能：抓取窗体截图，并返回图像内存数据
        参    数：
                 x 截取起始x坐标（窗体内相对坐标）
                 y 截取起始y坐标（窗体内相对坐标）
                 w 截取宽度,为0则取窗体宽度
                 h 截取长度,为0则取窗体高度
        """
        if self.win_hd is None:
            return None
        rect = self.getWinRect()
        if w == 0:
            w = rect.right - rect.left
        if h == 0:
            h = rect.bottom - rect.top
        if x < 0 or y < 0 or (x+w) > rect.right or (y+h) > rect.bottom:
            return None
        return self.Capture(self.win_hd, '', x, y, w, h, 1)

    def Capture(self, hd, path, x, y, w, h, mode):
        """
        函数功能：截图
        参    数：hd 截取的窗口句柄
                path 保存路径
                 x 截取起始x坐标（窗体内相对坐标）
                 y 截取起始y坐标（窗体内相对坐标）
                 w 截取宽度,为0则取窗体宽度
                 h 截取长度,为0则取窗体高度
                 mode 保存模式 0：保存为图片，1：返回图像字节数据
        """
        # 根据窗口句柄获取窗口的设备上下文
        hwndDC = win32gui.GetWindowDC(self.win_hd)
        # 根据窗口的DC获取memDC
        srcdc = win32ui.CreateDCFromHandle(hwndDC)
        # memDC创建可兼容的DC
        saveDC = srcdc.CreateCompatibleDC()
        # 创建bigmap准备保存图片
        saveBitMap = win32ui.CreateBitmap()
        # 为bitmap开辟空间
        saveBitMap.CreateCompatibleBitmap(srcdc, w, h)
        # 高度saveDC，将截图保存到saveBitmap中
        saveDC.SelectObject(saveBitMap)
        # 截取从左上角（0，0）长宽为（w，h）的图片
        saveDC.BitBlt((0, 0), (w, h), srcdc, (x, y), win32con.SRCCOPY)
        if mode == 0:
            saveBitMap.SaveBitmapFile(saveDC, path)
        else:
            signedIntsArray = saveBitMap.GetBitmapBits(True)
            return signedIntsArray
        # 释放内存
        srcdc.DeleteDC()
        saveDC.DeleteDC()
        win32gui.ReleaseDC(self.win_hd, hwndDC)
        win32gui.DeleteObject(saveBitMap.GetHandle())

    def EnumWindowsProc(self, hwnd, lParam):
        buffer = create_string_buffer(255, '\0')
        GetWindowText(hwnd, buffer, 255)
        value = buffer.value.decode('gbk')
        if value == self.win_title:
            self.win_hd = hwnd
            print(self.win_hd)
            return False
        return True


if __name__ == '__main__':
    import time
    import autopy
    form = FormControl()
    # autopy.mouse.smooth_move(100,100)
    # form.bindWindowByName(None,'*无标题 - 记事本')
    # form.bindWindowByName('l2UnrealWWindowsViewportWindow','Lineage II')
    form.bindWindowByName(None,'Lineage II')
    form.WindowActive()

    rect = form.getWinRect()
    print("坐标:（x:%d,y:%d）,大小:(width:%d,height:%d)" %
          (rect.left, rect.top, rect.right-rect.left, rect.bottom-rect.top))
    time.sleep(1)

    import pyautogui
    pyautogui.moveTo(100,100,duration=0.25)
    pyautogui.moveTo(200,100,duration=0.25)
    pyautogui.moveTo(200,200,duration=0.25)
    pyautogui.moveTo(100,200,duration=0.25)
    # autopy.key.tap(autopy.key.Code.F1,[autopy.key.Modifier.META])
    # autopy.key.type_string("WWWWW")
    
    autopy.mouse.smooth_move(444,697)
    # autopy.mouse.move(444,697)
    autopy.mouse.click()
    # autopy.mouse.click()
    print(autopy.mouse.location())
    # form.WinCapture(r'l:\1.bmp',0,0,200,200)

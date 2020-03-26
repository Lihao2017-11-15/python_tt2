import win32api
import win32con

import autopy
import struct
import threading
import serial
import time
import datetime
import sys


class HID(object):
    def __init__(self, x_rate=1, y_rate=1, com_port='COM3', com_baudrate=19200):
        self.x_rate = x_rate
        self.y_rate = y_rate
        self.port = com_port
        self.baudrate = com_baudrate
        self.ser = serial.Serial(self.port, self.baudrate)
        if self.ser.isOpen == False:
            ser.open()
            
    def __delattr__(self):
        self.close()

    def close(self):
        self.keyup()
        try:
            self.ser.close()
        except:
            pass

    def move(self, x, y):
        """
        命令包及应答包数据格式如下：
        帧头 地址码 命令码 后续数据长度 后续数据 累加和
        HEAD ADDR CMD LEN DATA SUM
        2 个字节 1 个字节 1 个字节 1 个字节 N 个字节(0-64) 1 个字节
        帧头：占 2 个字节，固定为 0x57、0xAB；
        地址码：占 1 个字节，默认为 0x00，可接收任意地址码的命令包，如果芯片地址设置成
        0x01---0xFE，则只能接收对应地址码或地址码为 0xFF 的命令包。0xFF 为广播包，芯片不需
        要进行应答；
        命令码：占 1 个字节，外围串口设备发起的帧的命令码有效范围为：0x01---0x3F，CH9329
        芯片发送正常应答包时的命令码为：原命令码 | 0x80；CH9329 芯片发送异常应答包时的命
        令码为：原命令码 | 0xC0；
        后续数据长度：占 1 个字节，主要用于记录该包实际后续数据的长度，仅包含后续数据
        外围串口设备
        (PC 机、MCU 等)
        CH9329 芯片 USB 主机
        (PC 机、平板等)
        CH9329 芯片串口通信协议 WCH 沁恒 4
        部分，不包括帧头字节、地址码、命令码和累加和字节；
        后续数据：占 N 个字节，N 有效范围为 0---64。
        累加和：占 1 个字节，计算方式为： SUM = HEAD+ADDR+CMD+LEN+DATA。

        表 1-命令码表
        命令名称 命名码 命令说明
        CMD_GET_INFO 0x01
        获取芯片版本等信息
        通过该命令向芯片获取版本号、
        USB 枚举状态、键盘大小写指示灯
        状态等信息
        CMD_SEND_KB_GENERAL_DATA 0x02
        发送 USB 键盘普通数据
        通过该命令向芯片发送普通键盘
        数据包，模拟普通按键按下或释放
        动作
        CMD_SEND_KB_MEDIA_DATA 0x03
        发送 USB 键盘多媒体数据
        通过该命令向芯片发送多媒体键
        盘数据包，模拟多媒体按键按下或
        释放动作
        CMD_SEND_MS_ABS_DATA 0x04
        发送 USB 绝对鼠标数据
        通过该命令向芯片发送绝对鼠标
        数据包，模拟绝对鼠标相关动作
        CMD_SEND_MS_REL_DATA 0x05
        发送 USB 相对鼠标数据
        通过该命令向芯片发送相对鼠标
        数据包，模拟相对鼠标相关动作
        CMD_SEND_MY_HID_DATA 0x06
        发送 USB 自定义 HID 设备数据
        通过该命令向芯片发送自定义 HID
        类设备数据包
        """
        head = b'\x57\xab'
        addr = b'\x00'
        cmd = b'\x04'
        len = b'\x07'
        data = b'\x02\x00'+self.__坐标转换(x, y)+b'\x00'
        _sum = sum(head + addr + cmd + len + data)
        _sum = struct.pack('B', self.__整数转字节码(_sum)[0])  # 将低字节转为bytes
        self.__send(head + addr + cmd + len + data + _sum)

    def click_left(self):
        # cmd1 = b'\x57\xAB\x00\x04\x07\x02\x01\x00\x00\x00\x00\x00\x10'
        # cmd2 = b'\x57\xAB\x00\x04\x07\x02\x00\x00\x00\x00\x00\x00\x0F'
        cmd1 = b'\x57\xAB\x00\x05\x05\x01\x01\x00\x00\x00\x0E'
        左键 = b'\x57\xAB\x00\x05\x05\x01\x01\x00\x00\x00\x0E'
        右键 = b'\x57\xAB\x00\x05\x05\x01\x00\x01\x00\x00\x0E'
        中键 = b'\x57\xAB\x00\x05\x05\x01\x00\x00\x01\x00\x0E'
        cmd2 = b'\x57\xAB\x00\x05\x05\x01\x00\x00\x00\x00\x0D'
        self.__send(cmd1)
        self.__send(cmd2)

    def click_center(self):
        # cmd1 = b'\x57\xAB\x00\x04\x07\x02\x00\x01\x00\x00\x00\x00\x10'
        # cmd2 = b'\x57\xAB\x00\x04\x07\x02\x00\x00\x00\x00\x00\x00\x0F'
        cmd1 = b'\x57\xAB\x00\x05\x05\x01\x01\x00\x00\x00\x0E'
        cmd2 = b'\x57\xAB\x00\x05\x05\x01\x00\x00\x00\x00\x0D'
        self.__send(cmd1)
        self.__send(cmd2)

    def click_right(self):
        cmd1 = b'\x57\xAB\x00\x04\x07\x02\x00\x00\x01\x00\x00\x00\x10'
        cmd2 = b'\x57\xAB\x00\x04\x07\x02\x00\x00\x00\x00\x00\x00\x0F'
        self.__send(cmd1)
        self.__send(cmd2)

    def sendkeys(self, key, releae=True):
        """按键,releae=True弹起"""
        是否为组合键 = False
        try:
            是否为组合键 = key.index("+") > 0
        except:
            pass
        if 是否为组合键:
            pass
        else:
            pass

    def keypress(self, key):
        self.keydown(key)
        self.keyup()

    def keydown(self, key):
        print(f"按下{key}")
        head = b'\x57\xab'
        addr = b'\x00'
        cmd = b'\x02\x08'
        len = b'\x00'
        data = b'\x00'+self.__getcode(key)+b'\x00\x00\x00\x00\x00'
        _sum = sum(head + addr + cmd + len + data)
        _sum = struct.pack('B', self.__整数转字节码(_sum)[0])  # 将低字节转为bytes
        buffer = head + addr + cmd + len + data + _sum
        # print(buffer.hex())
        self.__send(buffer)

    def keyup(self):
        """释放按键"""
        cmd = b'\x57\xAB\x00\x02\x08\x00\x00\x00\x00\x00\x00\x00\x00\x0C'  # 释放按键
        self.__send(cmd)

    def __getcode(self, key):
        if "ENTER" == key:
            return b'\x58'
        elif "↑" == key:
            return b'\x52'
        elif "↓" == key:
            return b'\x51'
        elif "←" == key:
            return b'\x50'
        elif "→" == key:
            return b'\x4F'
        elif "A" == key.upper():
            return b'\x04'
        elif "W" == key.upper():
            return b'\x1a'
        elif "1" == key:
            return b'\x1E'
        elif "ALT" == key.upper():
            return b'\xe6'
        elif "F1" == key.upper():
            return b'\x3A'
        elif "F2" == key.upper():
            return b'\x3b'
        elif "F3" == key.upper():
            return b'\x3c'
        elif "F4" == key.upper():
            return b'\x3d'
        elif "F5" == key.upper():
            return b'\x3e'
        elif "F6" == key.upper():
            return b'\x3f'
        elif "F7" == key.upper():
            return b'\x40'
        elif "F8" == key.upper():
            return b'\x41'
        elif "F9" == key.upper():
            return b'\x42'
        elif "F10" == key.upper():
            return b'\x43'
        elif "F11" == key.upper():
            return b'\x44'
        elif "F12" == key.upper():
            return b'\x45'

    def __send(self, cmd, wait_tim=0.1):
        response = b''
        totalsize = 0
        self.ser.write(cmd)
        size = self.ser.inWaiting()               # 获得缓冲区字符
        time.sleep(wait_tim)
        # if size != 0:
        #     while size != 0:
        #         response += self.ser.read(size)
        #         totalsize += size
        #         time.sleep(0.01)
        #         size = self.ser.inWaiting()
        # try:
        #     print(f'指令：{cmd},读取：{response},长度:{totalsize}字节')
        # except:
        #     pass
        self.ser.flushInput()                 # 清空接收缓存区

    def __坐标转换(self, x, y):
        screenW = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)  # 获得屏幕分辨率X轴
        screenH = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)  # 获得屏幕分辨率Y轴
        x = int(x * 4096 / screenW * self.x_rate)
        y = int(y * 4096 / screenH * self.y_rate)
        x = self.__整数转字节码(x)
        y = self.__整数转字节码(y)
        return x + y

    def __整数转字节码(self, x):
        """
        int.from_bytes(bytes, byteorder, *, signed=False)
        参数解释： bytes是要转换的十六进制；
        byteorder：选'big'和'little'，以上例为例，其中big代表正常顺序，即f1ff。little反之，代表反序fff1；
        signed：选True、Flase表示是否要区分二进制的正负数含义。即是否要对原二进制数进行原码反码补码操作。
        """
        return x.to_bytes(length=2, byteorder='little', signed=False)

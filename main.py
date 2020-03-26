# -*- coding: UTF-8 -*-
from inc.ai_qq_apiutil import *
import inc.ai_qq_apiutil as apiutil
import json
import colorsys
from random import *
from PIL import Image, ImageGrab, ImageFilter
from inc.FormAPI import *
from inc.kmAPI import *


def toScreenPos(*args):
    """窗口坐标转屏幕坐标"""
    if len(args) == 2:
        x1 = args[0]
        y1 = args[1]
        pos = form.toScreenPos(x1, y1)
        x1 = pos.x
        y1 = pos.y
        return x1, y1
    elif len(args) == 4:
        x1 = args[0]
        y1 = args[1]
        x2 = args[2]
        y2 = args[3]
        pos = form.toScreenPos(x1, y1)
        x1 = pos.x
        y1 = pos.y
        if x2 == 0 and y2 == 0:  # 截取整个窗口
            rect = form.getWinRect()
            return x1, y1, rect.right-rect.left, rect.bottom-rect.top
        pos = form.toScreenPos(x2, y2)
        x2 = pos.x
        y2 = pos.y
        return x1, y1, x2, y2
    else:
        raise "参数错误"


def move(x, y):
    """窗口坐标转屏幕坐标"""
    x, y = toScreenPos(x, y)
    hid.move(x, y)


def getallcolor(x, y):
    x, y = toScreenPos(x, y)
    color = hex(autopy.screen.get_color(x, y)).strip('0x')
    r = color[:2]
    g = color[2:4]
    b = color[4:6]
    return {"hexrgb": (b + g + r).upper(), "hexbgr": (r + g + b).upper(), "rgb": (int('0x'+r, 16), int('0x'+g, 16), int('0x'+b, 16))}


def rgb_tuple_tobgr(r, g, b):
    return bytes((b, g, r)).hex().upper()


def findcolor(x1, y1, x2, y2, bgrcolor):
    x1, y1, x2, y2 = toScreenPos(x1, y1, x2, y2)
    img = ImageGrab.grab((x1, y1, x2, y2))
    # print((x1, y1, x2, y2))
    # img.show()

    for x in range(0, img.size[0]):
        for y in range(0, img.size[1]):
            if rgb_tuple_tobgr(*img.getpixel((x, y))) in bgrcolor.upper().split("|"):
                img.close()
                return True
    img.close()
    return False


def getcolorlist(x1, y1, x2, y2):
    x1, y1, x2, y2 = toScreenPos(x1, y1, x2, y2)
    img = ImageGrab.grab((x1, y1, x2, y2))
    # img.show()
    角色坐标 = (img.size[0] // 2, img.size[1] // 2)
    ret = []
    list_pix = img.load()

    for x in range(0, img.size[0]):
        for y in range(0, img.size[1]):
            r, g, b = list_pix[x, y]
            if r > 255//3*2 and g <= 255//4 and b <= 255//4 and abs(x-角色坐标[0]) > 15 and abs(y-角色坐标[1]) > 15:
                ret.append((
                    (x-角色坐标[0]) ** 2+(y-角色坐标[1]) ** 2,  # 第一个参数用勾股定律，最小的值最近
                    x-角色坐标[0],
                    y-角色坐标[1],
                    (r, g, b)
                ))
    img.close()
    return sorted(ret)


def Ocr(x1, y1, x2, y2):
    x1, y1, x2, y2 = toScreenPos(x1, y1, x2, y2)
    img = ImageGrab.grab((x1, y1, x2, y2))
    ret = ExecTecentAPI(Apiname='ocr_generalocr', image=img)
    return ret


def ExecTecentAPI(*arg, **kwds):
    APPID = '2115475358'
    APPKEY = 'PMM4vvSPFsYI1kmA'

    if kwds.get('Apiname'):
        apiname = kwds.pop('Apiname')

    url = TencentAPI[apiname]['APIURL']
    name = TencentAPI[apiname]['APINAME']
    desc = TencentAPI[apiname]['APIDESC']
    para = TencentAPI[apiname]['APIPARA']

    tx = TencentAPIMsg(APPID, APPKEY)

    Req_Dict = {}
    for key in para.split(','):
        value = None
        #print (kwds)
        if kwds.get(key):
            value = kwds.pop(key)
        if key == 'image':
            # 图像获取base64
            value = tx.get_img_base64str(value)
        if key == 'text':
            # 文本进行GBK编码
            value = value.encode('gbk')

        Req_Dict[key] = value

    # 生成请求包
    sign = tx.init_req_dict(req_dict=Req_Dict)
    resp = requests.post(url, data=Req_Dict)
    # print(name+',API应答码:'+str(resp.json()['ret']))
    text = None
    try:
        for each in resp.json()['data']['item_list']:
            text = text + each['itemstring']
    except:
        text = None
    return text


def 是否选中怪物():
    return findcolor(580, 47, 589, 69, "13176F")


def 怪物是否掉血():
    flag = 0
    img1 = ImageGrab.grab(toScreenPos(576, 49, 736, 70))
    for _ in range(5):
        if not 是否选中怪物():
            return True
        time.sleep(1)
        img2 = ImageGrab.grab(toScreenPos(576, 49, 736, 70))
        if img1 != img2:
            flag = 0
            break
        else:
            flag += 1

    img2.close()
    img1.close()
    return flag == 0


def 自动拾取():
    hid.keydown("F4")
    time.sleep(random())
    hid.keyup()


def 找最近的怪():
    print("找最近的怪...")
    ret = getcolorlist(1085,34,1286,236)
    if len(ret) == 0:
        print("附近没怪？")
        return
    firstitem = ret[0]
    x = firstitem[1]
    y = firstitem[2]
    print(f"找到个{len(ret)}个怪物，最近的怪坐标：", x, y, firstitem[3])
    if x > 0:
        hid.keydown("→")
    elif x < 0:
        hid.keydown("←")
    time.sleep(abs(x)*0.05)
    # hid.keyup()
    if y > 0:
        hid.keydown("↓")
    elif y < 0:
        hid.keydown("↑")
    time.sleep(abs(y)*0.05)
    hid.keyup()


def 自动加buff():
    global 上次加buff时间
    if time.time() - 上次加buff时间 < 20*60:
        return
    print("自动加buff")

    move(683, 630)
    time.sleep(random())
    hid.click_left()
    hid.click_left()

    move(720, 631)
    time.sleep(random())
    hid.click_left()
    hid.click_left()

    move(759, 629)
    time.sleep(random())
    hid.click_left()
    hid.click_left()

    move(796, 628)
    time.sleep(random())
    hid.click_left()
    hid.click_left()

    上次加buff时间 = time.time()

if __name__ == "__main__":
    print("""
    注意事项：
    执行前取消雷达固定
    把雷达地图放大到1级

    背包第1格放返回卷轴
    """)
    global 上次加buff时间
    上次加buff时间 = 0
    hid = HID(x_rate=0.5)
    form = FormControl()
    # form.bindWindowByName(None, '*无标题 - 记事本')
    form.bindWindowByName(None, 'Lineage II')
    form.WindowActive()
    time.sleep(0.5)

    while True:
        form.bindActiveWindow()
        if form is not None:
            if form.getWinTitle() != "Lineage II":
                print("游戏窗口失去焦点，脚本停止")
                break
        else:
            print("当前焦点不是游戏窗口")

        if 是否选中怪物():
            print("找到怪物，开始攻击")
            hid.keypress("F1")
            while 是否选中怪物():
                hid.keydown("F2")
                if not 怪物是否掉血():
                    print("打不到")
                    # 找最近的怪()
                    print("查找怪物中...")
                    hid.keypress("F5")
                    break
            hid.keyup()

        # 自动加buff()
        自动拾取()
        for _ in range(2): # 按两次，一次有可能按键失败
            hid.keypress("F5")
            if 是否选中怪物():
                break
        else: # 如果两次都没找到怪
            # 找最近的怪()
            print("查找怪物中...")
            hid.keypress("F5")

    hid.close()
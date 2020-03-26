# -*- coding: utf-8 -*-

'''
create by : joshua zou
create date : 2017.11.28
Purpose: check tecent ai api
'''


from inc.ai_qq_apiutil import *
# 通用api构造函数


def ExecTecentAPI(*arg, **kwds):
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
        #print (key,value,Req_Dict[key])

    # 生成请求包
    sign = tx.init_req_dict(req_dict=Req_Dict)
    resp = requests.post(url, data=Req_Dict)
    print(name+',API应答码:'+str(resp.json()['ret']))
    text = ''
    try:
        for each in resp.json()['data']['item_list']:
            text = text+'/' + each['itemstring']
    except:
        text = ''
    return text



APPID = '100000000'
APPKEY = 'ZV1w000000'

if __name__ == "__main__":
    for file in glob.glob('D:\python\guoyaotang\*.jpg'):
        rest = ExecTecentAPI(Apiname='ocr_generalocr', image=file)
        print(file+rest)

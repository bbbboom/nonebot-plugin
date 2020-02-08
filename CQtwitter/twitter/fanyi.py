# -*- coding: UTF-8 -*-

import random
import hashlib
import urllib.request
import http.client
import json
####################
appid = ''  # 你的appid
secretKey = ''  # 你的密钥
####################
async def fan(x):
    if x=="":
        return "无内容"
    httpClient = None
    myurl = '/api/trans/vip/translate'
    q = x
    fromLang = 'jp'
    toLang = 'zh'
    salt = random.randint(32768, 65536)
    sign = appid + q + str(salt) + secretKey
    m1 =  hashlib.md5()
    m1.update(sign.encode("utf-8"))
    sign = m1.hexdigest()
    myurl = myurl + '?appid=' + appid + '&q=' + urllib.request.quote(q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
        salt) + '&sign=' + sign
    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)
        response = httpClient.getresponse()
        s=response.read()
        s.decode('utf-8')
        jsonData = json.loads(s)['trans_result']
        end=jsonData[0]['dst']
        return end
    finally:
        if httpClient:
            httpClient.close()

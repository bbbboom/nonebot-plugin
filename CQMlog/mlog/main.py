# -*- coding: utf-8 -*-

from . import utils
from .constant import *
import random
import os
import re


neteaseUrl = 'https://st.music.163.com/mlog/mlog.html'


async def handlingMessages(msg, bot, userGroup, userQQ):
    msg = await utils.cleanAt(msg)
    limitCharacter = ['Mlog', '发布了']
    if await matchingRules(msg, limitCharacter):
        url = await matchUrl(msg)
        if url:
            src = await tryToGetTheUrl(url)
            if src:
                src = src.replace('&', '%26')
                srcShort = await shortConnection(src)
                content = await utils.atQQ(userQQ)
                prefix = ['加入幸福一家人：', '神秘连接：', '加入相亲相爱一家人：']
                content += random.choice(prefix) + srcShort
                await bot.send_group_msg(group_id = int(userGroup), message = str(content))


async def moreAdvancedPackaging(msg, bot, userGroup, userQQ):
    try:
        await handlingMessages(msg, bot, userGroup, userQQ)
    except Exception as e:
        print(e)
    
async def matchUrl(msg):
    reg = re.compile(r'https?:\/\/(([a-zA-Z0-9_-])+(\.)?)*(:\d+)?(\/((\.)?(\?)?=?&?[a-zA-Z0-9_-](\?)?)*)*',flags = re.I)
    list = re.search(reg, msg)
    if list == None:
        return None
    if list.group(0).find(neteaseUrl) == -1:
        return None
    return list.group(0)


async def tryToGetTheUrl(url):
    p = './mlog/config/config.json'
    content = await utils.readJson(p)
    if content == FAILURE:
        raise Exception('缺少 config.json 文件')
    chrome = content['chrome']
    scriptLocation = './mlog/script/script.js'
    if not os.path.exists(scriptLocation):
        raise Exception('缺少脚本 script.js')
    os.system(f'node ./mlog/script/script.js "{url}" "{chrome}"')
    outPath = './mlog/script/out.json'
    if not os.path.exists(outPath):
        raise Exception('程序未执行成功')
    content = await utils.readJson(outPath)
    if content == FAILURE:
        raise Exception('读取 out.json 未成功')
    return content['src']
    
async def shortConnection(url):
    p = './mlog/config/key.json'
    content = await utils.readJson(p)
    if content == FAILURE:
        raise EOFError('缺少 key.json ')
    key = content['key']
    urlPath = f'http://suo.im/api.htm?format=json&key={key}&url={url}'
    content = await utils.asyncGet(urlPath)
    if content == FAILURE:
        raise Exception('转短连接失败')
    if content['err'] != "":
        raise Exception('短连接网站出错')
    return content['url']


async def matchingRules(msg, rules):
    mark = True
    for i in rules:
        if msg.find(i) == -1:
            mark = False
            break
    return mark
    

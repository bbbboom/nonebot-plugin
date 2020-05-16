# -*- coding:utf-8 -*-

import random
import aiohttp
import os
from . import utils

try:
    import ujson as json
except:
    import json

async def getMessage(bot, userGroup, msg):
    try:
        if msg == '一言':
            sendMsg = await getHtkt('default')
            sendMsg = sendMsg['hitokoto'] + '\nfrom ' + sendMsg['from']
            await bot.send_group_msg(group_id = userGroup, message = sendMsg)
        else:
            msg = msg.split(' ')
            if msg[0] == '一言':
                sendMsg = await getHtkt(str(msg[1]))
                sendMsg = sendMsg['hitokoto'] + '\nfrom ' + sendMsg['from']
                await bot.send_group_msg(group_id = userGroup, message = sendMsg)
    except:
        pass

async def backUp(msg):
    p = './hitokoto/data/backup.json'
    content = await utils.readFileToJSON(p)
    if content == 'error':
        os.mkdir(p.replace('/backup.json', ''))
        initialStructure = {
            'data': [],
            'number': 0
        }
        await utils.writeTo(p, initialStructure)
    if msg != '网络错误呢':
        content = await utils.readFileToJSON(p)
        content['data'].append(msg)
        content['number'] += 1
        await utils.writeTo(p, content)


async def getHtkt(type = 'default'):
    basePath = 'https://v1.hitokoto.cn/?c='
    if type == 'default':
        typeList = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
        basePath += random.choice(typeList)
    elif type == 'anime':
        basePath += 'a'
    elif type == 'comic':
        basePath += 'b'
    elif type == 'game':
        basePath += 'c'
    elif type == 'novel':
        basePath += 'd'
    elif type == 'myself':
        basePath += 'e'
    elif type == 'internet':
        basePath += 'f'
    elif type == 'other':
        basePath += 'g'
    else:
        basePath = basePath.replace('?c=', '')
    msg = await netGet(basePath)
    await backUp(msg)
    return msg
    

async def netGet(path):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url = path, timeout = 10) as res:
                jsonStr = await res.json()
                return jsonStr
    except:
        return '网络错误呢'
    
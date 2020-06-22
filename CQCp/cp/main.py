# -*- coding: utf-8 -*-

try:
    import ujson
except:
    import json as ujson
    
import os
import random
import aiofiles

async def getParameters(msg):
    try:
        list = msg.split(' ')
        if list[0] == 'cp' and len(list) == 3:
            return [True, list[1], list[2]]
    except:
        pass
    return [False]

async def readInfo(path):
    if os.path.exists(path):
        async with aiofiles.open(path, 'r', encoding='utf-8') as f:
            return ujson.loads((await f.read()).strip())
    raise Exception

async def getMessage(bot, userGroup, msg):
    parameter = await getParameters(msg)
    if parameter[0] == False:
        return
    content = await readInfo('./cp/data/content.json')
    content = random.choice(content['data']).replace('<攻>', parameter[1]).replace('<受>', parameter[2])
    await bot.send_group_msg(group_id = int(userGroup), message = str(content))

    
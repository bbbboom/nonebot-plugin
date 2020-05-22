# -*- coding: UTF-8 -*-

import aiofiles
import aiohttp
import random
from PIL import Image
import os
try:
    import ujson
except:
    import json as ujson

async def savePicture(img):
    p = './picrotating/data/pic.jpg'
    async with aiofiles.open(p, 'wb') as f:
        await f.write(img)


async def imageDownload(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers = headers) as res:
            img = await res.read()
    return img


async def imageProcessing():
    p = './picrotating/data/pic.jpg'
    p_ = '../data/image/picrotating.jpg'
    img = Image.open(p)
    randomDirection = [Image.ROTATE_90, Image.ROTATE_180, Image.ROTATE_270]
    turnAround = random.choice(randomDirection)
    img.transpose(turnAround).save(p_)


async def pictureRotation(msg, bot, userGroup):
    await folderDetection()
    mark = False
    for i in msg:
        if i['type'] == 'image':
            imgUrl = i['data']['url']
            mark = True
            break
    if mark:
        extract = random.randint(0, 100)
        if extract > 60:
            # Start saving pictures
            img = await imageDownload(imgUrl)
            await savePicture(img)
            # Read and rotate
            await imageProcessing()
            content = '[CQ:image,file=picrotating.jpg]'
            await bot.send_group_msg(group_id = userGroup, message = content)
            

async def folderDetection():
    p = './picrotating/data'
    if not os.path.exists(p):
        os.mkdir(p)


async def checkIfItIsBlocked(userGroup):
    p = './picrotating/config/shield.json'
    async with aiofiles.open(p, 'r', encoding = 'utf-8') as f:
        content = await f.read()
    content = ujson.loads(content)
    for i in content['group']:
        if str(i) == str(userGroup):
            return True
    return False
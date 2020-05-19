# -*- coding: utf-8 -*-

from . import utils
import random
import os
from .constant import *

async def beAt():
    p = './bionics/data/tips/at.json'
    return await utils.randomListSelection(p, 'data')

async def echo():
    p = './bionics/data/tips/echo.json'
    return await utils.randomListSelection(p, 'data')

async def repeatInterruption():
    p = './bionics/data/tips/repeater.json'
    return await utils.randomListSelection(p, 'data')

async def messageDetection(msg, bot, userGroup):
    send = ''
    if await utils.whetherAtBot(msg):
        send = await beAt()
    elif msg.find('亲爱的') != -1:
        send = await echo()
    if send == '':
        return
    await bot.send_group_msg(group_id = userGroup, message = send)

async def repeatTheMainProgramInterruption(msg, userGroup, bot):
    p = './bionics/data/repeater'
    if not os.path.exists(p):
        os.mkdir(p)
    p += '/' + str(userGroup) + '.json'
    content = await utils.readJson(p)
    if content == FAILURE:
        messageStructure = {
            'data': msg,
            'number': 1
        }
        await utils.writeJson(p, messageStructure)
        return
    if msg == content['data']:
        if content['number'] == 5:
            send = await repeatInterruption()
            await bot.send_group_msg(group_id = userGroup, message = send)
            content['number'] = 0
            await utils.writeJson(p, content)
            return
        content['number'] += 1
        await utils.writeJson(p, content)


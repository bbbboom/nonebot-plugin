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

async def messageDetection(msg, bot, userGroup, userQQ):
    p = './bionics/data/config/shield.json'
    for i in (await utils.readJson(p))['qq']:
        if str(i) == str(userQQ):
            return
    send = ''
    if await utils.whetherAtBot(msg):
        send = await beAt()
    elif msg.find('亲爱的') != -1:
        # Prevent frequent triggering
        if await timingDevice('testing'):
            send = await echo()
            await timingDevice('recording')
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
        if content['number'] == 4:
            send = await repeatInterruption()
            await bot.send_group_msg(group_id = userGroup, message = send)
            content['number'] = 0
            content['data'] = send
            await utils.writeJson(p, content)
            return
        content['number'] += 1
        await utils.writeJson(p, content)
    else:
        content['data'] = msg
        await utils.writeJson(p, content) 

async def timingDevice(model = 'recording'):
    p = './bionics/data/config/timeLimit.json'
    if model == 'recording':
        await utils.timeToFile(p, await utils.getAccurateTimeNow())
    else:
        # First check if there is a file
        content = await utils.readJson(p)
        if content == FAILURE:
            return True
        lastTime = await utils.timeReadFromFile(p)
        timeDifference = (await utils.getTimeDifference(lastTime, model = SECOND))
        if timeDifference > await utils.parameterReadingAndWriting('timeInterval'):
            return True
        return False

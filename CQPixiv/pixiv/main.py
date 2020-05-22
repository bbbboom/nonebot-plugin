# -*- coding: utf-8 -*-

from . import utils
from .constant import *
from .get import GetPictures
import asyncio

async def downloadResourcesBasedOnId(id):
    info = SUCCESS
    try:
        base = await getBase()
        await base.oneTimeIncome(id)
    except:
        info = FAILURE
    return info

async def sendPictures(userGroup, bot):
    imageUrl = await GetPictures.randomSelection('completelyRandom')
    if imageUrl == FAILURE:
        return
    content = '[CQ:image,file=' + imageUrl + ']'
    
    message = await bot.send_group_msg(group_id = userGroup, message = content)
    messageID = message['message_id']
    await asyncio.sleep(30)
    await bot.delete_msg(message_id = messageID)

async def getBase():
    p = './pixiv/data/account.json'
    content = await utils.readJson(p)
    if content == FAILURE:
        raise Exception
    if content['account'] == '' or content['password'] == '':
        raise Exception
    return GetPictures(content['account'], content['password'])

async def checkTheMessage(msg, bot, userGroup, userQQ):
    drawingCommand = ['cu', 'Cu', '图来', '色图来', '不够色']
    back = await utils.commandMatching(msg, drawingCommand)
    if back['mark']:
        await sendPictures(userGroup, bot)
    
    getResourceCommand = ['kkp']
    p = './pixiv/data/administrators.json'
    if await utils.authorityInspection(p, userQQ):
        back = await utils.commandMatching(msg, getResourceCommand, BLURRY)
        if back['mark']:
            info = await downloadResourcesBasedOnId(int(back['command']))
            if info == SUCCESS:
                content = '收集成功，不愧是你'
            else:
                content = '收集失败，狗妈的否定.jpg'
            await bot.send_group_msg(group_id = userGroup, message = content)

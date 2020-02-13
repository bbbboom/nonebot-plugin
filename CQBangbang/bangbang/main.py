# -*- coding:utf-8 -*- 
from . import usualGet
from . import mapGet
import os

async def getNew(bot):
    new = await usualGet.new(await usualGet.get())
    if new == 'empty':
        return
    else:
        sendQunPath = 'bangbang_data/send.txt'
        if os.path.exists(sendQunPath):
            with open(sendQunPath,'r') as f:
                lines = f.readlines()
            for line in lines:
                qun = int(line.strip())
                await bot.send_msg(group_id=int(qun),message=str(new))

async def serchMap(bot,qun,id):
    songInfo = await usualGet.serch(id)
    if songInfo != 0 :
        await bot.send_msg(group_id=int(qun),message=str(songInfo))

async def getMap(bot,qun,id):
    await mapGet.mapGet(id,bot,qun)

async def qunShield(qun):
    txtPath = 'bangbang_data/qunShield.txt'
    if os.path.exists(txtPath):
        with open(txtPath,'r') as f:
            lines = f.readlines()
            for line in lines:
                if int(qun) == int(line.strip()):
                    return 0
    return 1
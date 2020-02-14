# -*- coding:utf-8 -*- 
from . import usualGet
from . import mapGet
import os
import aiofiles

# 查新
async def getNew(bot):
    new = await usualGet.new(await usualGet.get(1))
    if new == 'empty':
        return
    else:
        sendQunPath = 'bangbang_data/send.txt'
        if os.path.exists(sendQunPath):
            async with aiofiles.open(sendQunPath,'r') as f:
                lines = await f.readlines()
            for line in lines:
                qun = int(line.strip())
                await bot.send_msg(group_id=int(qun),message=str(new))

# 按名字查找
async def searchKey(bot,qun,key):
    songInfo = await usualGet.searchName(str(key))
    await bot.send_msg(group_id=int(qun),message=str(songInfo))

# 详细信息查询
async def searchMap(bot,qun,id):
    songInfo = await usualGet.search(id)
    if songInfo != 0 :
        await bot.send_msg(group_id=int(qun),message=str(songInfo))

# 简短信息查询
async def baseSearch(bot,qun,id):
    songInfo = await usualGet.base(id)
    if songInfo != 0:
        await bot.send_msg(group_id=int(qun),message=str(songInfo))

# 作谱
async def getMap(bot,qun,id):
    await mapGet.mapGet(id,bot,qun)

# 屏蔽群
async def qunShield(qun):
    txtPath = 'bangbang_data/qunShield.txt'
    if os.path.exists(txtPath):
        async with aiofiles.open(txtPath,'r') as f:
            lines = await f.readlines()
            for line in lines:
                if int(qun) == int(line.strip()):
                    return 0
    return 1
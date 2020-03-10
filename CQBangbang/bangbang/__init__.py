# -*- coding: UTF-8 -*-
from nonebot import *
from aiocqhttp.exceptions import Error as CQHttpError
from . import main
from . import command

bot = get_bot()

@scheduler.scheduled_job('interval', minutes =1)
async def new():
    await main.getNew(bot)

@bot.on_message("group")
async def bestdori(context):
    qun = context["group_id"]
    shield = await main.qunShield(int(qun))
    if shield == 1:
        msg = str(context["message"])
        # base info
        baseKeyList = ['k','kp','kkp']
        code = await command.reasonable(msg,baseKeyList)
        if code[0] == 1:
            await main.baseSearch(bot,qun,code[1])
        # detail info
        detailKeyList = ['serch','search']
        code = await command.reasonable(msg,detailKeyList)
        if code[0] == 1:
            await main.searchMap(bot,qun,code[1])
        # get map
        mapKeyList = ['map']
        code = await command.reasonable(msg,mapKeyList)
        if code[0] == 1:
            await main.getMap(bot,qun,code[1])
        # name search
        nameKeyList = ['s','sp','ssp']
        code = await command.reasonable(msg,nameKeyList,model='searchName')
        if code[0] == 1:
            await main.searchKey(bot,qun,code[1])
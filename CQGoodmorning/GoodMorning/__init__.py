# -*- coding: utf-8 -*-

from nonebot import *
from . import initialization
from . import match

bot = get_bot()

@bot.on_message("group")
async def entranceFunction(context):
    msg = str(context["message"])
    userQQ = context["user_id"]
    userGroup = context["group_id"]
    await match.starter(bot)
    await match.mainProgram(bot, userQQ, userGroup, msg)
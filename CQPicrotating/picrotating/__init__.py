# -*- coding: UTF-8 -*-

from nonebot import *
from . import main

bot = get_bot()

@bot.on_message("group")
async def _(context):
    msg = context["message"]
    userGroup = context["group_id"]
    if not await main.checkIfItIsBlocked(userGroup):
        await main.pictureRotation(msg, bot, userGroup)

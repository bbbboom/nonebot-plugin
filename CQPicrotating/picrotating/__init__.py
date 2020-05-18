# -*- coding: UTF-8 -*-

from nonebot import *
from . import main

bot = get_bot()

@bot.on_message("group")
async def _(context):
    msg = context["message"]
    userGroup = context["group_id"]
    await main.pictureRotation(msg, bot, userGroup)

# -*- coding: utf-8 -*-

from nonebot import *
from . import main
from . import utils

bot = get_bot()

@bot.on_message("group")
async def entranceFunction(context):
    msg = str(context["message"])
    userGroup = context["group_id"]
    userQQ = context["user_id"]
    await utils.initialization()
    await main.messageDetection(msg, bot, userGroup, userQQ)
    await main.repeatTheMainProgramInterruption(msg, userGroup, bot)

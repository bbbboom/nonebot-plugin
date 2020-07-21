# -*- coding: utf-8 -*-

from nonebot import *
from . import main
from . import utils

bot = get_bot()

@bot.on_message("group")
async def entranceFunction(context):
    try:
        msg = context["message"][0]['data']['text']
    except:
        return
    userGroup = context["group_id"]
    userQQ = context["user_id"]
    await utils.initialization()
    await main.moreAdvancedPackaging(msg, bot, userGroup, userQQ)

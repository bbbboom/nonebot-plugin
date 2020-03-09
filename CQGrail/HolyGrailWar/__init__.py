# -*- coding: utf-8 -*-

from nonebot import *
from . import polymerization

bot = get_bot()


@bot.on_message("group")
async def entranceFunction(context):
    msg = str(context["message"])
    userQQ = context["user_id"]
    userGroup = context["group_id"]
    rawMsg = context['message']
    await polymerization.aggregationCall(bot, userQQ, userGroup, msg, rawMsg)

# -*- coding: UTF-8 -*-
from nonebot import *
from . import time_t

bot = get_bot()

@scheduler.scheduled_job('cron', second = '30')
async def _time():
    await time_t.list(bot)

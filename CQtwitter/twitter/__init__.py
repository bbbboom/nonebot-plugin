# -*- coding: UTF-8 -*-
from nonebot import *
from . import time_t
from nonebot.permission import *
from aiocqhttp.exceptions import Error as CQHttpError

bot = get_bot()

@scheduler.scheduled_job('interval', minutes =1)
async def _time():
    await time_t.list(bot)

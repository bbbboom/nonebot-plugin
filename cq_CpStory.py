# -*- coding: utf-8 -*-

from nonebot import on_command, CommandSession
from nonebot import get_bot, log, permission
from . import common

import os
import random

__plugin_name__ = 'CP小故事'
__plugin_usage__ = r"""
[CP 小故事]
文案来自“mxh-mini-apps”
https://github.com/mxh-mini-apps/mxh-cp-stories
----------
直接使用：
    /cp {主角A} {主角B}
"""

# 获取bot对象
bot = get_bot()
pwd = os.path.dirname(__file__)

@on_command('cp', aliases=('cp'), only_to_me=False)
async def _loveword(session: CommandSession):
    # 获取参数链接
    arg = session.current_arg_text.strip()
    if not arg:
        # 向用户发送信息
        await session.send('故事不能没有主角')
        return
    
    # 整理参数
    arg = arg.replace('  ', ' ')
    arg = arg.replace('  ', ' ')
    arg = arg.replace('  ', ' ')
    args = arg.split(' ')
    if len(args) < 2:
        # 向用户发送信息
        await session.send('还缺个主角B')
        return
    
    # 读取模板
    tplPath = pwd + '/cq_CpStory.json'
    content = await common.readJson(tplPath)
    if content == None:
        await session.send('故事丢了')
        return
    
    # 开始生成
    content = random.choice(content['data'])
    content = content.replace('<攻>', args[0])
    content = content.replace('<受>', args[1])
    
    # 向用户发送信息
    await session.send(content)

# -*- coding: utf-8 -*-

from nonebot import on_command, CommandSession
from nonebot import get_bot, log, permission
from . import common

import os

__plugin_name__ = '营销号文案生成器'
__plugin_usage__ = r"""
[营销号文案生成器]
----------
用法：
    /yxh {主体} {事件} {另一种解释}
"""

# 获取bot对象
bot = get_bot()
pwd = os.path.dirname(__file__)

@on_command('yxh', aliases=('营销号'), only_to_me=False)
async def _yxh(session: CommandSession):
    # 获取参数字符串
    arg = session.current_arg_text.strip()
    if not arg:
        # 向用户发送信息
        await session.send('参数不足，营销失败！')
        return
    
    # 整理参数
    arg = arg.replace('  ', ' ')
    arg = arg.replace('  ', ' ')
    arg = arg.replace('  ', ' ')
    
    # 读取参数
    args = arg.split(' ')
    p_subject   = args[0] if len(args) >= 1 else ''
    p_event     = args[1] if len(args) >= 2 else ''
    p_statement = args[2] if len(args) >= 3 else p_subject + p_event
    
    # 组装文本
    content = ( '　　[subject][event]是怎么回事呢？[subject]相信大家都很熟悉，' +
                '但是[subject][event]是怎么回事呢，下面就让小编带大家一起了解吧。\n' +
                '　　[subject][event]，其实就是[statement]，大家可能会很惊讶[subject]' +
                '怎么会[event]呢？但事实就是这样，小编也感到非常惊讶。\n' +
                '　　这就是关于[subject][event]的事情了，大家有什么想法呢，欢迎在群聊告诉小编一起讨论哦！')
    content = content.replace('[subject]', p_subject)
    content = content.replace('[event]', p_event)
    content = content.replace('[statement]', p_statement)
    
    # 向用户发送信息
    await session.send(content)

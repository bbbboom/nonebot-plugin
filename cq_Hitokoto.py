# -*- coding: utf-8 -*-

from nonebot import on_command, CommandSession
from nonebot import get_bot, log, permission
from . import common

import aiocqhttp
import os

__plugin_name__ = '一言'
__plugin_usage__ = r"""
[一言]
----------
直接使用：
    /yan
    高低给爷整两句
指定句子类型：
    /yan 动画
    /yan 漫画
    /yan 游戏
    /yan 文学
    /yan 原创
    /yan 网络
    /yan 其他
    /yan 影视
    /yan 诗词
    /yan 网易云
    /yan 哲学
    /yan 抖机灵
"""

# 获取bot对象
bot = get_bot()
pwd = os.path.dirname(__file__)

@on_command('yan', aliases=('一言'), only_to_me=False)
async def _yan(session: CommandSession):
    # 获取参数链接
    arg = session.current_arg_text.strip()
    res = await getRes(arg)
    
    # 向用户发送信息
    await session.send(res)

@bot.on_message('group')
async def _show(event: aiocqhttp.Event):
    msg = str(event['message']).strip()
    if msg == '高低给爷整两句':
        res = await getRes('')
        group_id = event['group_id']
        await bot.send_group_msg(group_id = group_id, message = res)

async def getRes(arg):
    # 链接基本信息
    basePath = 'https://v1.hitokoto.cn/'
    typeDict = {
        '动画': 'a', '漫画': 'b', '游戏': 'c', '文学': 'd',
        '原创': 'e', '网络': 'f', '其他': 'g', '影视': 'h',
        '诗词': 'i', '网易云': 'j', '哲学': 'k', '抖机灵': 'l'}
    
    # 获取参数链接
    if arg != '':
        select = typeDict.get(arg)
        if select != None:
            # 如果在参数列表则返回指定类型地址
            basePath = basePath + '?c=' + select
    
    # 获取请求结果
    recvMsg = await common.getJson(basePath)
    
    # 组装信息格式
    sendMsg = '容我想想'
    if recvMsg != None:
        if recvMsg['from_who'] == None:
            recvMsg['from_who'] = ''
        sendMsg = '%s\n—— %s《%s》' % (recvMsg['hitokoto'], recvMsg['from_who'], recvMsg['from'])
    
    return sendMsg

# -*- coding: utf-8 -*-

from nonebot import on_command, CommandSession
from nonebot import get_bot, log, permission
from nonebot import plugin, get_loaded_plugins

import os, sys

# 获取bot对象
bot = get_bot()

# on_command 装饰器将函数声明为一个命令处理器
@on_command('usage', aliases=['help', '帮助', '使用帮助', '使用方法'], only_to_me=False)
async def _(session: CommandSession):
    # 获取插件列表
    plugins = get_loaded_plugins()
    
    # 需要从帮助列表隐藏的插件
    skipkey = ['nonebot.plugins.base', 'plugins.common', 'plugins.group', 'plugins.system']
    
    # 为没有名称的插件设置临时名称
    for key in list(plugins):
        if key.module.__name__ in skipkey:
            # 屏蔽指定插件
            plugins.remove(key)
        elif key.name == None:
            key.name = key.module.__name__
            key.name = key.name.replace('plugins.cq_', '')
            key.name = key.name.replace('plugins.', '')
    
    # 为插件列表进行排序
    plugins = sorted(plugins, key=lambda p: p.name, reverse=False)
    
    # 获取参数字符串
    arg = session.current_arg_text.strip().lower()
    if not arg:
        # 如果用户没有发送参数，则发送功能列表
        await session.send(
            '[现在支持的功能有]：\n'
            + '\n'.join(p.name for p in plugins)
            + '\n--------------------'
            + '\n发送"/usage {插件名}"获取插件的具体用法。'
        )
        return
    
    # 如果发了参数则发送相应命令的使用帮助
    for p in plugins:
        if p.name.lower() == arg:
            if p.usage == None:
                p.usage = '暂无相关用法！'
            await session.send(p.usage.strip())
            return
    await session.send('插件名输入错误！')

# on_command 装饰器将函数声明为一个命令处理器
@on_command('restart', aliases=('重启'), only_to_me=False, permission=permission.SUPERUSER)
async def _(session: CommandSession):
    plugins = get_loaded_plugins()
    for key in plugins:
        # 重启已经加载的插件(按插件名)
        log.logger.info('正在重载：' + key.module.__name__)
        plugin.reload_plugin(key.module.__name__)
    
    # 向用户发送帮助信息
    await session.send('所有插件重启完成')

# on_command 装饰器将函数声明为一个命令处理器
@on_command('shutdown', aliases=('关闭系统'), only_to_me=False, permission=permission.SUPERUSER)
async def _(session: CommandSession):
    # 向用户发送帮助信息
    await session.send('正在退出')
    
    # 执行命令
    sys.exit(0)
    
    # 获取内部的 Quart 对象
    app = bot.server_app
    # await app.shutdown()

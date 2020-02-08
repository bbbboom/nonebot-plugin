# -*- coding: UTF-8 -*-
import os

async def qunfa(name,bot,str):
    #遍历群
    if not os.path.exists('twitterConfig/qun.txt'):
        return
    else:
        with open('twitterConfig/qun.txt', 'r') as n:
            for line in n.readlines():
                line = line.strip()
                line = line.split(" ")
                if name==line[1]:
                    qun = line[0]
                    await bot.send_group_msg(group_id=int(qun), message=str, auto_escape=False)

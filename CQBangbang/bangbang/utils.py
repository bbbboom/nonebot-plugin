# -*- coding:utf-8 -*- 

async def stringLenLimit(s):
    if len(str(s)) > 131:
        return 0
    else:
        return 1


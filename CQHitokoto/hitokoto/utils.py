# -*- coding:utf-8 -*-

import os
import aiofiles

try:
    import ujson as json
except:
    import json

async def readFileToJSON(p):
    if not os.path.exists(p):
        return 'error'
    async with aiofiles.open(p, 'r', encoding='utf-8') as f:
        content = await f.read()
    content = json.loads(content)
    return content


async def writeTo(p, info):
    async with aiofiles.open(p, 'w', encoding='utf-8') as f:
        await f.write(json.dumps(info))


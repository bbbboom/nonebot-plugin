# -*- coding: UTF-8 -*-

import os

async def re(qun,msg):
    mark = 0
    msg = str(msg)
    p="repeater_data/"+str(qun)+".txt"
    if msg.find(".jpg")!=-1 or msg.find(".JPG")!=-1:
        return 0
    else:
        if os.path.exists(p):
            with open(p,"r",encoding="utf-8") as f:
                msg_old = f.read().strip()
            if msg_old == msg:
                mark=1
                with open(p, "w", encoding="utf-8") as f:
                    f.write("")
        if mark==0:
            with open(p,"w",encoding="utf-8") as f:
                    f.write(msg)
        return mark

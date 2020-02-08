# -*- coding:utf-8 -*-

import os,json

async def getIni(name,item):
    img = "image_data/"+str(name)+"/config.ini"
    with open(img,"r",encoding="utf-8") as f:
        ini = f.read()
    dic =  json.loads(ini)
    return dic[item]

async def getQqName(qq):
    p = "image_data/qqdata/"+str(qq)+".ini"
    mark = "initial"
    if os.path.exists(p):
        with open(p,"r",encoding="utf-8") as f:
            mark =f.read().strip()
    return mark

async def setQqName(qq,msg):
    item=0
    msg=str(msg)
    msg_list = msg.split(" ")
    if msg_list[0]=="img":
        mark = str(getQqName(qq))
        msg = msg_list[1]
        p="image_data/qqdata/"+str(qq)+".ini"
        name = "image_data/bieming/name.ini"
        if os.path.exists(name):
            with open(name,"r",encoding="gbk") as f:
                line = f.readlines()
                for i in line:
                    i = i.strip()
                    line_list=i.split(" ")
                    if line_list[0]==msg:
                        mark = line_list[1]
                        item=1
                        with open(p,"w",encoding="utf-8") as f:
                            f.write(str(mark))
    return item


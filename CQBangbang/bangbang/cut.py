# -*- coding:utf-8 -*- 
import os
# import requests
import aiohttp
import time
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

async def info(status,title = '',artists = '',cover = '',level = '',timestamp = '',author = '',songTime = '',id = '',comRatio = 3):
    if status == 1:
        # basic parameters
        scale = 0.2
        margin = int(200 * scale)
        lineDistance = int(290 * scale)
        # specialDistance = lineDistance * 2
        font = ImageFont.truetype("simhei.ttf",30)
        width = int(20*scale)+2*margin+7*lineDistance
        borderDistance = 50
        height = width + borderDistance * 10
        p = 'bangbang_data/'
        coverPath = '../data/image/bestdoriMap_' + str(id) + '.jpg'
        timestamp = time.localtime(timestamp/1000)
        timestamp = (str(timestamp.tm_year) + '/' +
                    str(timestamp.tm_mon) + '/' +
                    str(timestamp.tm_mday) + ' ' +
                    str(timestamp.tm_hour) + ':' +
                    str(timestamp.tm_min))
        m, s = divmod(songTime, 60)
        if str(s)[1] == '.':
            s = '0' + str(s)[0]
        else:
            s = str(s)[0:2]
        songTime = str(int(m)) + ':' + str(s)

        async with aiohttp.ClientSession() as session:
            async with session.get(cover) as res:
                with open(coverPath, 'wb') as f:
                    while 1:
                        chunk = await res.content.read(1024)    #每次获取1024字节
                        if not chunk:
                            break
                        f.write(chunk)

        background = Image.open(p+"static/bk.png").resize((width,height))
        image = Image.open(coverPath).convert('RGBA').resize((int(width-2*borderDistance),int(width-2*borderDistance)))
        background.paste(image,(borderDistance,borderDistance),image)
        infoText = ('Music: ' + str(title) +
                    '\n\nArtists: ' + str(artists) +
                    '\n\nID: ' + str(id) +
                    '\n\nLevel: ' + str(level) +
                    '\n\nTime: ' + str(songTime) +
                    '\n\nAuthor: ' + str(author) +
                    '\n\nUpdate: ' + str(timestamp))
        draw = ImageDraw.Draw(background)
        draw.text((borderDistance,width),infoText, 'white', font)
        comRatio = int(comRatio)
        return background.resize((int(width/comRatio),int(height/comRatio)))
    else:
        try:
            # basic parameters
            scale = 0.2
            margin = int(200 * scale)
            lineDistance = int(290 * scale)
            # specialDistance = lineDistance * 2
            font = ImageFont.truetype("simhei.ttf",30)
            width = int(20*scale)+2*margin+7*lineDistance
            borderDistance = 50
            height = width + borderDistance * 10
            p = 'bangbang_data/'
            coverPath = p + "static/cover.png"
            timestamp = time.localtime(timestamp/1000)
            timestamp = (str(timestamp.tm_year) + '/' +
                        str(timestamp.tm_mon) + '/' +
                        str(timestamp.tm_mday) + ' ' +
                        str(timestamp.tm_hour) + ':' +
                        str(timestamp.tm_min))
            m, s = divmod(songTime, 60)
            if str(s)[1] == '.':
                s = '0' + str(s)[0]
            else:
                s = str(s)[0:2]
            songLong = str(int(m)) + ':' + str(s)
            background = Image.open(p+"static/bk.png").resize((width,height))
            image = Image.open(coverPath).convert('RGBA').resize((int(width-2*borderDistance),int(width-2*borderDistance)))
            background.paste(image,(borderDistance,borderDistance),image)
            infoText = ('Music: ' + str(title) +
                        '\n\nArtists: ' + str(artists) +
                        '\n\nID: ' + str(id) +
                        '\n\nLevel: ' + str(level) +
                        '\n\nTime: ' + str(songTime) +
                        '\n\nAuthor: ' + str(author) +
                        '\n\nUpdate: ' + str(timestamp))
            draw = ImageDraw.Draw(background)
            draw.text((borderDistance,width),infoText, 'white', font)
            comRatio = int(comRatio)
            return background.resize((int(width/comRatio),int(height/comRatio)))
        except:
            return 'error'

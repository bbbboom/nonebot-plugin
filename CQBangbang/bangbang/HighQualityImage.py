# -*- coding:utf-8 -*- 
import os
import requests
import json
import time
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

########################################################################
'''
    单独使用此文件前
    一、必须确保你已经安装了相关依赖
        pip install requests
        pip install pillow
    二、不可移动此文件位置，确保在 ../bangbang_data/static/ 内有静态资源
        （如果你没有移动过，可忽略此步）
    三、如果你的电脑内存 <= 4 GB ，请谨慎调整参数，质量太高文件会过大，
        如果卡死长按电源键强制关机即可
'''

# 核心参数 设定以下四个即可
# 谱面 id
id = 8119
# 压缩参数-压缩百分比 | 高质量图可以设定为 1(不压缩)或2(压缩一倍)
comRatio = 2
# 音轨剪断节数 | 一般 2-4 min 歌曲设定为 8-12 若歌曲特别短 如 1 min 可设定为更小值 不建议小于 5 
cutNumber = 12
# 压缩参数-画面质量 | 一般设定为 50-100
imageQuality = 80

'''
    以 id = 7070 为例 (曲长 4 min)
    设定压缩比 = 2 ， 画面质量 = 80
    得到的图片有 2 MB
    设定压缩比 = 1 (相当于不压缩)， 画面质量 = 100 (100%不压缩的画面质量)
    得到的图片有 8 MB
'''
########################################################################
def cutInfo(status,title = '',artists = '',cover = '',level = '',timestamp = '',author = '',songTime = '',id = ''):
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
        p = '../bangbang_data/'
        coverPath =  str(id) + '_cover.jpg'
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
        imageCover = requests.get(cover, stream=True)
        open(coverPath, 'wb').write(imageCover.content)
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
        return background
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
            p = '../bangbang_data/'
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
            return background
        except:
            return 'error'


def mapGet(id):
    # map image path
    imageP = str(id) + '.jpg'
    # static path
    p = '../bangbang_data/'
    # json get
    jsonStr = requests.get('https://bestdori.com/api/post/details?id=' + str(id)).json()
    if jsonStr['result']!=True:
        print('谱面获取失败，请检查网络')
        return
    # 做底图
    # 压缩比例 - 不要更改
    scale = 0.2
    # 边距
    margin = int(200 * scale)
    # notes
    notes = jsonStr['post']['notes']
    # info
    if type(jsonStr['post']['graphicsSimulator'][-1]['time']) is list:
        songTime = jsonStr['post']['graphicsSimulator'][-1]['time'][0]
    else:
        songTime = jsonStr['post']['graphicsSimulator'][-1]['time']
    author = jsonStr['post']['author']['username']
    timestamp = jsonStr['post']['time']
    level = jsonStr['post']['level']
    artists = jsonStr['post']['artists']
    title = jsonStr['post']['title']
    try:
        # info封面
        cover = jsonStr['post']['song']['cover']
        cutStatus = cutInfo(1,title,artists,cover,level,timestamp,author,songTime,id)
    except:
        cutStatus = cutInfo(0,title = title,artists = artists,cover = '',level = level,
        timestamp = timestamp,author = author,songTime = songTime,id = id) 
    try:
        maxBeat = notes[-1]['beat']
    except:
        print('谱面有错误')
        return
    # note上下距离
    noteLength = int(600 * scale)
    # 作底图
    lineLength = noteLength * (int(maxBeat)+1) 
    lineDistance = int(290 * scale)
    height = lineLength+margin*2
    width = int(20*scale)+2*margin+7*lineDistance
    background = Image.open(p+"static/bk.png").resize((width,height))
    line = Image.open(p+'static/line.png').resize((int(5*scale),lineLength))
    lineB = Image.open(p+'static/line.png').resize((int(20*scale),lineLength))
    crossLine = Image.open(p+'static/line.png')
    lineLangB = Image.open(p+'static/lineLang.png').resize((lineDistance,int(30*scale)))
    lineBpm = Image.open(p+'static/lineBpm.png').resize((lineDistance*8,int(10*scale)))
    for i in range(0,8):
        if i == 0 or i == 7:
            background.paste(lineB,(margin+i*lineDistance,margin))
        else:
            background.paste(line,(margin+i*lineDistance,margin))
    # 作icon
    iconNote = Image.open(p+'static/note.png')
    iconLang = Image.open(p+'static/lang.png')
    iconJump = Image.open(p+'static/jump.png')
    draw = ImageDraw.Draw(background)
    font = ImageFont.truetype("consola.ttf",20)
    color = (31, 92, 51)
    posLockA,posA = 0,[0,0,0,0]
    posLockB,posB = 0,[0,0,0,0]
    backA,backB = [0,0],[0,0]
    halfLang = 115*scale/2
    xSEO = int(15*scale)
    contiguousNote = [0,0]
    halfNote = int(305*scale/2)
    halfHeight = int(110*scale/2) - int(5*scale)
    startMarkA,startMarkB = 0,0
    # icon上图
    for note in notes:
        if note['type'] == 'Note':
            if note['note'] == 'Single':
                try:
                    if note['flick'] == True:
                        background.paste(iconJump,(margin+(int(note['lane'])-1)*lineDistance,
                        int(lineLength+margin-noteLength*note['beat'])),iconJump)
                except:
                    # 同按线
                    if (note['beat'] == contiguousNote[0]) and (note['lane'] != contiguousNote[1]):
                        crossLine = crossLine.resize((abs(note['lane']-contiguousNote[1])*lineDistance,int(10*scale)))
                        minNoteLane = note['lane']
                        if note['lane']>contiguousNote[1] :
                            minNoteLane = contiguousNote[1]
                        background.paste(crossLine,(margin+(minNoteLane-1)*lineDistance+halfNote,
                        int(lineLength+margin-noteLength*note['beat']+halfHeight)))
                        background.paste(iconNote,(margin+(int(contiguousNote[1])-1)*lineDistance,
                        int(lineLength+margin-noteLength*contiguousNote[0])),iconNote)
                    background.paste(iconNote,(margin+(int(note['lane'])-1)*lineDistance,
                    int(lineLength+margin-noteLength*note['beat'])),iconNote)
                    contiguousNote[0],contiguousNote[1] = note['beat'],note['lane']
            elif note['note'] == 'Slide':
                if note['pos'] == 'A':
                    try :
                        if note['start'] == True:
                            # start lang
                            posA[0],posA[1] = note['beat'],note['lane']
                            background.paste(iconLang,(margin+(int(note['lane'])-1)*lineDistance,
                            int(lineLength+margin-noteLength*note['beat'])),iconLang)
                            # back
                            startMarkA = 1
                            backA[0],backA[1] = note['beat'],note['lane']
                    except:
                        try:
                            if note['end'] == True:
                                # end lang
                                posA[2],posA[3] = note['beat'],note['lane']
                                # backA = [0,0]
                                draw.polygon([(posA[1]-1)*lineDistance+margin+xSEO,int(lineLength+margin-noteLength*posA[0]+halfLang),
                                posA[1]*lineDistance+margin-xSEO,int(lineLength+margin-noteLength*posA[0]+halfLang),
                                posA[3]*lineDistance+margin-xSEO,int(lineLength+margin-noteLength*posA[2]+halfLang),
                                (posA[3]-1)*lineDistance+margin+xSEO,int(lineLength+margin-noteLength*posA[2]+halfLang)],fill=color,)
                                posLockA = 0
                                background.paste(iconLang,(margin+(int(note['lane'])-1)*lineDistance,
                                int(lineLength+margin-noteLength*note['beat'])),iconLang)
                                # 重画
                                if startMarkA == 1:
                                    background.paste(iconLang,(margin+(int(backA[1])-1)*lineDistance,
                                    int(lineLength+margin-noteLength*backA[0])),iconLang)
                                    startMarkA = 0
                                else:
                                    background.paste(lineLangB,(margin+(int(backA[1])-1)*lineDistance,
                                    int(lineLength+margin-noteLength*backA[0]+halfLang)))
                        except:
                            posA[2],posA[3] = note['beat'],note['lane']
                            draw.polygon([(posA[1]-1)*lineDistance+margin+xSEO,int(lineLength+margin-noteLength*posA[0]+halfLang),
                            posA[1]*lineDistance+margin-xSEO,int(lineLength+margin-noteLength*posA[0]+halfLang),
                            posA[3]*lineDistance+margin-xSEO,int(lineLength+margin-noteLength*posA[2]+halfLang),
                            (posA[3]-1)*lineDistance+margin+xSEO,int(lineLength+margin-noteLength*posA[2]+halfLang)],fill=color,)
                            posA[0],posA[1] = note['beat'],note['lane']
                            # 本条
                            background.paste(lineLangB,(margin+(int(note['lane'])-1)*lineDistance,
                            int(lineLength+margin-noteLength*note['beat']+halfLang)))
                            if startMarkA == 1:
                                background.paste(iconLang,(margin+(int(backA[1])-1)*lineDistance,
                                int(lineLength+margin-noteLength*backA[0])),iconLang)
                                startMarkA = 0
                            else:
                                background.paste(lineLangB,(margin+(int(backA[1])-1)*lineDistance,
                                int(lineLength+margin-noteLength*backA[0]+halfLang)))
                            # 记录本身
                            backA[0],backA[1] = note['beat'],note['lane']
                elif note['pos'] == 'B':
                    try :
                        if note['start'] == True:
                            # start lang
                            posB[0],posB[1] = note['beat'],note['lane']
                            background.paste(iconLang,(margin+(int(note['lane'])-1)*lineDistance,
                            int(lineLength+margin-noteLength*note['beat'])),iconLang)
                            # back
                            startMarkB = 1
                            backB[0],backB[1] = note['beat'],note['lane']
                    except:
                        try:
                            if note['end'] == True:
                                # end lang
                                posB[2],posB[3] = note['beat'],note['lane']
                                # backA = [0,0]
                                draw.polygon([(posB[1]-1)*lineDistance+margin+xSEO,int(lineLength+margin-noteLength*posB[0]+halfLang),
                                posB[1]*lineDistance+margin-xSEO,int(lineLength+margin-noteLength*posB[0]+halfLang),
                                posB[3]*lineDistance+margin-xSEO,int(lineLength+margin-noteLength*posB[2]+halfLang),
                                (posB[3]-1)*lineDistance+margin+xSEO,int(lineLength+margin-noteLength*posB[2]+halfLang)],fill=color,)
                                posLockB = 0
                                background.paste(iconLang,(margin+(int(note['lane'])-1)*lineDistance,
                                int(lineLength+margin-noteLength*note['beat'])),iconLang)
                                # 重画
                                if startMarkB == 1:
                                    background.paste(iconLang,(margin+(int(backB[1])-1)*lineDistance,
                                    int(lineLength+margin-noteLength*backB[0])),iconLang)
                                    startMarkB = 0
                                else:
                                    background.paste(lineLangB,(margin+(int(backB[1])-1)*lineDistance,
                                    int(lineLength+margin-noteLength*backB[0]+halfLang)))
                        except:
                            posB[2],posB[3] = note['beat'],note['lane']
                            draw.polygon([(posB[1]-1)*lineDistance+margin+xSEO,int(lineLength+margin-noteLength*posB[0]+halfLang),
                            posB[1]*lineDistance+margin-xSEO,int(lineLength+margin-noteLength*posB[0]+halfLang),
                            posB[3]*lineDistance+margin-xSEO,int(lineLength+margin-noteLength*posB[2]+halfLang),
                            (posB[3]-1)*lineDistance+margin+xSEO,int(lineLength+margin-noteLength*posB[2]+halfLang)],fill=color,)
                            posB[0],posB[1] = note['beat'],note['lane']
                            # 本条
                            background.paste(lineLangB,(margin+(int(note['lane'])-1)*lineDistance,
                            int(lineLength+margin-noteLength*note['beat']+halfLang)))
                            if startMarkB == 1:
                                background.paste(iconLang,(margin+(int(backB[1])-1)*lineDistance,
                                int(lineLength+margin-noteLength*backB[0])),iconLang)
                                startMarkB = 0
                            else:
                                background.paste(lineLangB,(margin+(int(backB[1])-1)*lineDistance,
                                int(lineLength+margin-noteLength*backB[0]+halfLang)))
                            # 记录本身
                            backB[0],backB[1] = note['beat'],note['lane']
                else:
                    print('谱面轨道错误')
                    return 
        else:
            background.paste(lineBpm,(margin,
            int(lineLength+margin-noteLength*note['beat']+halfHeight)))
            draw.text((margin+7*lineDistance+int(50*scale),
            int(lineLength+margin-noteLength*note['beat']+halfHeight+int(50*scale))), str(note['bpm']), 'violet', font)
    # 美化边距
    marginPlus = margin
    plusWidth = width*(cutNumber + 1) 
    plusHeight = int(height/cutNumber) 
    backgroundPlus = Image.open(p+"static/bk.png").resize((plusWidth+marginPlus*2,plusHeight+marginPlus*2))
    for i in range(cutNumber):
        backgroundPlus.paste(background.crop((0,height-(i+1)*plusHeight,width,height-i*plusHeight)),
        ((i+1)*width+marginPlus,marginPlus))
    if cutStatus != 'error':
        # 加封面
        backgroundPlus.paste(cutStatus,(marginPlus,marginPlus+int(plusHeight/2-(width+500)/2))) # 500 = borderDistance * 10
    # 来源
    fontSource = ImageFont.truetype("consola.ttf",25)
    drawPlus = ImageDraw.Draw(backgroundPlus)
    drawPlus.text((30,plusHeight+marginPlus-10), 'Source: Bestdori - collectBot', 'white', fontSource)

    #存图片
    backgroundPlus.resize((int((plusWidth+marginPlus*2)/comRatio),int((plusHeight+marginPlus*2)/comRatio))).convert('RGB').save(imageP,quality=imageQuality) 

    return 


if __name__ == '__main__':
    mapGet(id)

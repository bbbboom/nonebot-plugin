# -*- coding:utf-8 -*- 
import os
import requests
import json
import time

# get新谱列表
async def get():
    url = 'https://bestdori.com/api/post/list'
    header = {'content-type': 'application/json;charset=UTF-8'}
    postData = {"following":False,"categoryName":"SELF_POST","categoryId":"chart","order":"TIME_DESC","limit":20,"offset":0}
    jsonStr = requests.post(url,data=json.dumps(postData),headers = header).json()
    if jsonStr['result'] != True:
        print('requests lose')
        return 'error'
    return jsonStr['posts']

# 查新
async def new(songs):
    mark = 0
    newSongs = ''
    savePath = 'bangbang_data/save.txt'
    if songs != 'error':
        if os.path.exists(savePath):
            with open(savePath,'r') as f:
                saveSongs = f.read()
                for song in songs:
                    songID = song['id']
                    if saveSongs.find(str(songID)) != -1:
                        # 存在
                        break
                    else:
                        # 不在
                        if newSongs != '':
                            newSongs += '\n'
                        songLong = song
                        newSongs += ('【新谱' + str(song['id']) +'】\n' +
                                        'Music: ' + str(song['title']) + '\n' +
                                        'Level: ' + str(song['level']) + '\n' +
                                        'Author: ' + str(song['author']['nickname']) + '\n'
                                        '介绍: '
                                        )
                        for j in song['content']:
                            if j['type'] == 'text':
                                newSongs += str(j['data']) + ' '
            if newSongs != '':
                mark = 1
    with open(savePath,'w') as f:
        songIDs = ''
        for song in songs:
            songIDs += str(song['id']) + '\n'
        f.write(songIDs)
    if mark == 1:
        return newSongs
    return 'empty'

# 定向详细info
async def serch(id):
    # 查缓存
    jsonPath = 'bangbang_data/' + str(id) + '.json'
    if os.path.exists(jsonPath):
        # 有缓存
        pass
    else:
        # get
        try:
            jsonStr = requests.get('https://bestdori.com/api/post/details?id=' + str(id)).json()
            if jsonStr['result']!=True:
                print('serch:get失败')
                return 0
            # 写缓存
            with open(jsonPath,'w') as f:
                f.write(json.dumps(jsonStr))
        except:
            return 
    # 读缓存
    with open(jsonPath,'r',encoding='utf-8') as f:
        jsonStr = json.loads(f.read())
    # send msg
    songInfo = ''
    post = jsonStr['post']
    uptime = post['time']
    songLong = post['graphicsSimulator'][-1]['time']
    # cover下载
    try:
        imagePath = '../data/image/bestdori_' + str(id) + '.jpg'
        if os.path.exists(imagePath):
            songInfo += '[CQ:image,file=bestdori_'+ str(id) + '.jpg]\n'
        else:
            # 下载
            imageCover = requests.get(post['song']['cover'], stream=True)
            open(imagePath, 'wb').write(imageCover.content)
            songInfo += '[CQ:image,file=bestdori_'+ str(id) + '.jpg]\n'
    except:
        songInfo += '封面获取失败\n'
    # 时间格式化
    uptime = time.localtime(uptime/1000)
    uptime = (str(uptime.tm_year) + '/' +
                str(uptime.tm_mon) + '/' +
                str(uptime.tm_mday) + ' ' +
                str(uptime.tm_hour) + ':' +
                str(uptime.tm_min))
    m, s = divmod(songLong, 60)
    songLong = str(int(m)) + ':' + str(s)[3:5]
    # 添加信息
    songInfo += ('Music: ' + str(post['title']) + '\n' + 
                'Artists: ' + str(post['artists']) + '\n' + 
                'Level: ' + str(post['level']) + '\n' + 
                'ID: ' + str(id) + '\n' +
                'Time: ' + str(songLong) + '\n' +
                'Author: ' + str(post['author']['nickname']) + '\n'
                'Update: ' + str(uptime) + '\n' +
                '介绍: '
                )
    for j in post['content']:
        if j['type'] == 'text':
            songInfo += str(j['data']) + ' '
    return songInfo

    

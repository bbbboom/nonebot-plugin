# -*- coding: UTF-8 -*-

import requests,os
from . import fanyi
from . import fun
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
####################
async def name_set(msg,name):
    p = "twitterConfig/fy_plus.txt"
    if os.path.exists(p):
        with open(p,"r") as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip().split(" ")
                try:
                    if name == line[0]:
                        old = line[1]
                        new = line[2]
                        msg = msg.replace(old,new)
                except:
                    pass
    return msg


async def twitter(x,y,url,name,bot):
    fatui = str(name)+'发布了新推文！\n--------------------\n'
    zhuanfa = str(name)+'转发了推文！\n--------------------\n'
    path='../data/image/'
    if x > y:
        if url != None:
                page= requests.get(url)
                soup = BeautifulSoup(page.content, 'html.parser')
                #print(soup.prettify())
                #推文状态
                tw_=soup.find_all('div', class_='context',limit=x)[y].get_text()
                #推文
                tw = soup.find_all('div', class_='content',limit=x)[y].find('p',class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').get_text()
                tw = tw.replace(' …','')
            #原文链接获取
                wei=''
                if tw.find('pic.twitter.com')!=-1:
                    wei=tw[tw.find('pic.twitter.com'):].replace('pic.twitter.com','原文链接:https://t.co')
                    tw=tw[0:tw.find('pic.twitter.com')]
                #翻译
                fy=tw.replace("\n","")
                fy=fy[0:fy.find('http')]
                fy = await name_set(fy,name)
                fy=await fanyi.fan(fy)
                fy='翻译:'+fy
            #媒体
                g=0 #媒体数量
                mt=soup.find_all('div', class_='content',limit=x)[y].find_all("div",class_='AdaptiveMedia-photoContainer')
                if mt!=None:
                    for i in range(len(mt)):
                        urlretrieve(mt[i].find("img")['src'],path+str(g)+'_'+str(name)+'.jpg')
                        g+=1
                #正文
                tw='正文:'+tw
                if tw_=='\n':
                    tw = fatui+tw
                else:
                    tw = zhuanfa+tw
                #汇总
                end=tw+'\n'+fy
                #第1波文
                await fun.qunfa(name,bot,end)
                end2=''
                if g>0:
                    end2+='图片:\n'
                    for i in range(g):
                        end2+='[CQ:image,file='+str(i)+'_'+str(name)+'.jpg]'
                        if i!=g:
                            end2+='\n'
                    end2 += wei
                    #第2波文
                    await fun.qunfa(name,bot,end2)



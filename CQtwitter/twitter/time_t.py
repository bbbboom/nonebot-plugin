# -*- coding: UTF-8 -*-
from . import twitter
import requests
import os
from bs4 import BeautifulSoup
####################

async def list(bot):
    p = "twitterConfig/user.txt"
    if os.path.exists(p):
        with open(p,"r") as f:
            lines = f.readlines()
            for line in lines:
                user = line.strip().split(" ")
                url = "https://twitter.com/"+str(user[0])
                nick = user[0]
                x = int(user[1])
                y = int(user[2])
                name = user[3]
                await main(nick,x,y,url,name,bot)


async def main(nick,x,y,url,name,bot):
    if x>y:
        if url!=None:
                page= requests.get(url)
                soup = BeautifulSoup(page.content, 'html.parser')
                #取时间
                sj=soup.find_all('div', class_='content',limit=x)[y].find("div",'stream-item-header').find('a',class_='tweet-timestamp js-permalink js-nav js-tooltip')
                sj=sj['title']
                t=''
                p = 'twitterConfig/new_time_'+str(nick)+'.txt'
                if not os.path.exists(p):
                    with open(p,'w') as f:
                        f.write(sj)
                else:
                    with open(p, 'r') as f1:
                        t=f1.read()
                    t=t.strip()
                    sj=sj.strip()
                    if t!=sj:
                        #存时间
                        with open(p,'w') as f2:
                            f2.write(sj)
                        #发推
                        await twitter.twitter(x,y,url,name,bot)

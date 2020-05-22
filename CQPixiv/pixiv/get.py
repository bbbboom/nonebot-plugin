# -*- coding: utf-8 -*-

from pixivpy3 import *
from . import utils
from .constant import *
import random

class GetPictures():

    def __init__(self, account, password):
        self.api = ByPassSniApi()
        self.api.require_appapi_hosts()
        self.api.set_accept_language('zh-cn')
        self.api.login(account, password)

    async def __getAllPictures(self, id):
        result = {
            "data": [],
            "number": 0,
            "next_url": []
        }
        offset = 0
        mark = True
        while mark:
            json_result = self.api.user_illusts(id, offset = offset)
            result['data'] += json_result['illusts']
            result['number'] += 1
            if json_result['next_url'] == None:
                mark = False
            result['next_url'].append(json_result['next_url'])
            # print(json_result['next_url'])
            offset += 30
        return result

    async def __organizePictures(self, result):
        newResult = {
            "data": [],
            "number": 0,
            "count": 0
        }
        for i in result['data']:
            newStructure = {
                'id': i['id'],
                'count': i['page_count'],
                'url': [],
                'url_large': [],
                'cat_url': [],
                'cat_url_large': []
            }
            newStructure['count'] = i['page_count']
            newStructure['id'] = i['id']
            # url
            if 'original_image_url' in i['meta_single_page']:
                newStructure['url'].append(i['meta_single_page']['original_image_url'])
                newStructure['url_large'].append(i['image_urls']['large'])
            else:
                for j in i['meta_pages']:
                    newStructure['url'].append(j['image_urls']['original'])
                    newStructure['url_large'].append(j['image_urls']['large'])
            # cat_url
            for j in newStructure['url']:
                newStructure['cat_url'].append(j.replace('i.pximg.net', 'i.pixiv.cat'))
            for j in newStructure['url_large']:
                newStructure['cat_url_large'].append(j.replace('i.pximg.net', 'i.pixiv.cat'))
            newResult['data'].append(newStructure)
            newResult['number'] += 1
            newResult['count'] += newStructure['count']
        return newResult

    async def oneTimeIncome(self, id):
        path = './pixiv/data/images/' + str(id) + '.json'
        await utils.checkFolder(path)
        newResult = await self.__organizePictures(await self.__getAllPictures(id))
        await utils.writeJson(path, newResult)

    @staticmethod
    async def randomSelection(model = 'completelyRandom', id = ''):
        path = './pixiv/data/images/'
        if model == 'completelyRandom':
            path = await utils.randomlyExtractedFromTheFolder(path)
        if model == 'precise':
            path += str(id) + '.json'

        content = await utils.readJson(path)
        if content == FAILURE:
            return FAILURE
        return random.choice(random.choice(content['data'])['cat_url'])

            
            

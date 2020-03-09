# -*- coding: utf-8 -*-

import os
import ujson
import random
import aiofiles
from . import Utils
from . import Utils2
from . import Utils3
from . import Utils3plus
from . import initialization
from .customException import GrailExcept

error = 'error'
ok = 'ok'

async def readTheSpecifiedFollowerInformationInTheRecordPool(userQQ, followQQ):
    p = './HolyGrailWar/User/Servant/RecordPool.json'
    content = await Utils.readFileToJSON(p)
    if content == error:
        return error
    for c in content['recordlist']:
        if c['master'] == userQQ and c['qq'] == followQQ:
            return c
    return error


async def extractRankingDataFromTheSharedPool():
    p = './HolyGrailWar/User/Servant/SharePool.json'
    content = await Utils.readFileToJSON(p)
    if content == error:
        return error
    countList = []
    for c in content['sharelist']:
        mark = 0
        for l in countList:
            if l['follow_qq'] == c['follow_qq']:
                mark = 1
                l['number'] += 1
                break
        if mark == 0:
            countingStructure = {
                "follow_qq": c['follow_qq'],
                "number": 1
            }
            countList.append(countingStructure)
    countList.sort(key = lambda x:x['number'], reverse = True)
    return countList


async def checkIfLeaderboardIsAvailable(userGroup, model):
    p = './HolyGrailWar/User/Ranking/' + str(userGroup) + '.json'
    content = await Utils.readFileToJSON(p)
    if content == error:
        fileStructure = {
            "share_leaderboard": "2017-10-01/00:00:00",
            "gold_coin_ranking": "2017-10-01/00:00:00",
            "fighting_leaderboard": "2017-10-01/00:00:00",
            "follower_qualifications_list": "2017-10-01/00:00:00"
        }
        await Utils.writeTo(p, fileStructure)
        content = await Utils.readFileToJSON(p)
    timeDifference = await Utils3plus.judgeTimeDifference(content[model])
    if timeDifference >= 60 * 10:
        return 1
    return 0


async def setLeaderboardQueryTags(userGroup, model):
    p = './HolyGrailWar/User/Ranking/' + str(userGroup) + '.json'
    content = await Utils.readFileToJSON(p)
    if content == error:
        raise GrailExcept
    content[model] = await Utils3plus.getAccurateTime()
    await Utils.writeTo(p, content)
    return ok


async def followerRankings(userQQ, userGroup):
    msg = await Utils.atQQ(userQQ)
    # Set query CD
    await setLeaderboardQueryTags(userGroup, 'share_leaderboard')
    msg += 'Servant 热度排行榜:\n*同一个群内，10分钟只能查询一次排行榜\n\n' 
    countList = await extractRankingDataFromTheSharedPool()
    if countList == error:
        return msg + '暂时没有人捕捉随从哦'
    impressionCap = await Utils3.customParameterReading('shared_leaderboard_display_cap')
    for index, c in enumerate(countList):
        followInfo = await Utils.userInformationQuery(c['follow_qq'])
        if followInfo == error:
            raise GrailExcept
        if index + 1 == 1:
            msg += '🥇'
        elif index + 1 == 2:
            msg += '🥈'
        elif index + 1 == 3:
            msg += '🥉'
        else:
            msg += str(index + 1)
        msg += ('. ' + followInfo['register']['register_group_business_card'] + '\n' + 
                '   - 热度：' + str(c['number']) + '\n')
        if index + 1 == impressionCap:
            break
    return msg


async def extractingRecordPoolData():
    p = './HolyGrailWar/User/Servant/RecordPool.json'
    content = await Utils.readFileToJSON(p)
    if content == error:
        return error
    followList = content['recordlist']
    followList.sort(key = lambda x:x['combat_effectiveness']['initial_fighting_power'], reverse = True)
    return followList


async def getGroupName(bot, userGroup):
    groupInfo = await bot.get_group_info(group_id = userGroup)
    return groupInfo['group_name']


async def followerQualificationsList(bot, userQQ, userGroup):
    msg = await Utils.atQQ(userQQ)
    # Set query CD
    await setLeaderboardQueryTags(userGroup, 'follower_qualifications_list')
    followList = await extractingRecordPoolData()
    msg += ('Servant 资质排行榜:\n*资质仅展示随从的初始战斗力排行，不包括共享战斗力\n' + 
            '*同一个群内，10分钟只能查询一次排行榜\n\n')
    if followList == error:
        return msg + '暂时没有人捕捉随从哦'
    impressionCap = await Utils3.customParameterReading('maximum_number_of_follower_qualifications')
    for index, f in enumerate(followList):
        masterInfo = await Utils.userInformationQuery(f['master'])
        if masterInfo == error:
            raise GrailExcept
        if index + 1 == 1:
            msg += '🥇'
        elif index + 1 == 2:
            msg += '🥈'
        elif index + 1 == 3:
            msg += '🥉'
        else:
            msg += str(index + 1)
        msg += ('. ' + f['name'] + '(战斗力：' + 
                str(f['combat_effectiveness']['initial_fighting_power']) + ')\n' +
                '   - Master：' + masterInfo['register']['register_group_business_card'] + '\n' +
                '   - 捕捉地点：' + await getGroupName(bot, f['arrest_time']['catch_group']) + 
                '(' + f['arrest_time']['capture_group_code'] + ')\n')
        if index + 1 == impressionCap:
            break
    return msg


async def getAListOfAllUsers():
    userList = os.listdir('./HolyGrailWar/User/Data')
    return userList


async def goldCoinRanking(userQQ, userGroup):
    msg = await Utils.atQQ(userQQ)
    await setLeaderboardQueryTags(userGroup, 'gold_coin_ranking')
    msg += 'Master 金币排行榜:\n*资质仅展示随从的初始战斗力排行，不包括共享战斗力\n\n'
    impressionCap = await Utils3.customParameterReading('the_maximum_number_of_impressions_on_the_gold_coin_ranking')
    userFileNameList = await getAListOfAllUsers()
    if userFileNameList == []:
        return error
    goldList = []
    for u in userFileNameList:
        p = u[:u.find('.')]
        userInfo = await Utils.userInformationQuery(p)
        if userInfo == error:
            raise GrailExcept
        userGoldCoinStructure = {
            "qq": userInfo['qq'],
            "name": userInfo['register']['register_group_business_card'],
            "gold": userInfo['resources']['gold']
        }
        goldList.append(userGoldCoinStructure)
    goldList.sort(key = lambda x:x['gold'], reverse = True)
    for index, f in enumerate(goldList):
        if index + 1 == 1:
            msg += '🥇'
        elif index + 1 == 2:
            msg += '🥈'
        elif index + 1 == 3:
            msg += '🥉'
        else:
            msg += str(index + 1)
        msg += ('. ' + f['name'] + '(' + str(f['qq']) + ')\n' + 
                '   - 金币：' + str(f['gold']) + '\n')
        if index + 1 == impressionCap:
            break
    return msg


async def userCombatDataExtraction():
    userCombatList = []
    userFileNameList = await getAListOfAllUsers()
    for u in userFileNameList:
        p = u[:u.find('.')]
        userInfo = await Utils.userInformationQuery(p)
        if userInfo == error:
            raise GrailExcept
        combatEffectiveness = await Utils3plus.statisticsOfSingleCombatPower(int(p), 0)
        code = await initialization.getOrWriteNumber(0, userInfo['game']['last_game_time_group'],
                                                                                model = 'group')
        userStructure = {
            "qq": userInfo['qq'],
            "name": userInfo['register']['register_group_business_card'],
            "group": userInfo['game']['last_game_time_group'],
            "code": code,
            "combat_effectiveness": combatEffectiveness
        }
        userCombatList.append(userStructure)
    userCombatList.sort(key = lambda x:x['combat_effectiveness'], reverse = True)
    return userCombatList


async def fightingLeaderboard(bot, userQQ, userGroup):
    msg = await Utils.atQQ(userQQ)
    await setLeaderboardQueryTags(userGroup, 'fighting_leaderboard')
    msg += 'Master 战斗力排行榜:\n*该榜单展示 Master 的战斗力排行，战斗力大部分来自于随从\n*同一个群内，10分钟只能查询一次排行榜\n\n'
    impressionCap = await Utils3.customParameterReading('fighting_leaderboard_display_limit')
    userCombatList = await userCombatDataExtraction()
    for index, f in enumerate(userCombatList):
        if index + 1 == 1:
            msg += '🥇'
        elif index + 1 == 2:
            msg += '🥈'
        elif index + 1 == 3:
            msg += '🥉'
        else:
            msg += str(index + 1)
        msg += ('. ' + f['name'] + '(' + str(f['qq']) + ')\n' + 
                '   - 战斗力：' + str(f['combat_effectiveness']) + '\n' +
                '   - 最近活跃群：' + await getGroupName(bot, f['group']) + 
                '(' + f['code'] + ')\n')
        if index + 1 == impressionCap:
            break
    return msg


async def summaryFunction(bot, userQQ, userGroup, model):
    status = await checkIfLeaderboardIsAvailable(userGroup, model)
    if status == 1:
        if model == 'share_leaderboard':
            msg = await followerRankings(userQQ, userGroup)
        if model == 'gold_coin_ranking':
            msg = await goldCoinRanking(userQQ, userGroup)
        if model == 'fighting_leaderboard':
            msg = await fightingLeaderboard(bot, userQQ, userGroup)
        if model == 'follower_qualifications_list':
            msg = await followerQualificationsList(bot, userQQ, userGroup)
        return msg.strip()
    return error
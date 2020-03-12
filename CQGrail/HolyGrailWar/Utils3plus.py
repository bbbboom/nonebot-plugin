# -*- coding: utf-8 -*-

import os
import ujson
import random
import aiofiles
from dateutil.parser import parse
import datetime
from . import Utils
from . import Utils2
from . import Utils3
from . import initialization
from .customException import GrailExcept

error = 'error'
ok = 'ok'

async def updateAllSharedData(userQQ):
    user = await Utils.userInformationQuery(userQQ)
    if user == error:
        raise GrailExcept
    entourage = user['entourage']
    if entourage['number'] == 0:
        return error
    for e in entourage['follower_information']:
        e['combat_effectiveness']['shared_combat_effectiveness'] = await Utils3.computingSharedForces(e['qq'])
        e['combat_effectiveness']['share_number'] = await Utils3.getTheNumberOfShares(e['qq'])
        # Ranking refresh
        e['combat_effectiveness']['ranking'] = await Utils3.refreshRecordPoolRanking(e['master'], e['qq'])
    # Write back
    user['entourage'] = entourage
    await Utils.writeUserInformation(userQQ, user)
    return ok


async def followerList(userQQ):
    entourage = await Utils3.getInformationOfUserSFollowerModule(userQQ)
    p = './HolyGrailWar/Config/UserAssistance/Entourage.json'
    content = await Utils.readFileToJSON(p)
    if content == error:
        raise GrailExcept
    msg = await Utils.atQQ(userQQ)
    number = await Utils3.judgeWhetherToBeArrested(userQQ, 0, model = 'maximum_value')
    msg += content['prefix'] + str(number) + '\n\n' + content['line'] + '\n'
    if entourage['number'] == 0:
        msg += '空空如也\n' + content['line'] + '\n'
    else:
        random.shuffle(content['emoji'])
        count = 0
        # Refresh shared data
        status = await updateAllSharedData(userQQ)
        entourage = await Utils3.getInformationOfUserSFollowerModule(userQQ)
        if status == error:
            return error
        for e in entourage['follower_information']:
            msg += (content['emoji'][count] + e['name'] + '：\n战斗力：' + 
                    str(e['combat_effectiveness']['initial_fighting_power']) + '(基础+' +
                    str(e['combat_effectiveness']['basics']) + '，' + '技能+' + 
                    str(e['combat_effectiveness']['skill']['total_combat_strength']) + ')\n' +
                    '  共享战斗力：+' + str(e['combat_effectiveness']['shared_combat_effectiveness']) +
                    '（共享平衡-' + 
                    str(await Utils3.computingSharedForces(e['qq'], model = 'shared_balance')) +
                    '%）\n' + '  全服排名：')
            if e['combat_effectiveness']['ranking'] > 200:
                msg += '千里之外'
            else:
                msg += str(e['combat_effectiveness']['ranking'])
            msg += ('\n' + '技能：' + '[' + e['combat_effectiveness']['skill']['name'] + e['combat_effectiveness']['skill']['quality']['name'] + 
                    ']\n' + content['line'] + '\n')
            count += 1
    msg += content['suffix']
    return msg
                    

async def cleanUpTheRecordPool(userQQ, followQQ):
    p = './HolyGrailWar/User/Servant/RecordPool.json'
    content = await Utils.readFileToJSON(p)
    if content == error:
        raise GrailExcept
    designatedLocation = 0
    for index, r in enumerate(content['recordlist']):
        if r['master'] == userQQ and r['qq'] == followQQ:
            designatedLocation = index
    del content['recordlist'][designatedLocation]
    content['number'] -= 1
    await Utils.writeTo(p, content)
    return ok


async def deleteSharePool(userQQ, followQQ):
    p = './HolyGrailWar/User/Servant/SharePool.json'
    content = await Utils.readFileToJSON(p)
    if content == error:
        raise GrailExcept
    designatedLocation = 0
    for index, r in enumerate(content['sharelist']):
        if r['qq'] == userQQ and r['follow_qq'] == followQQ:
            designatedLocation = index
    del content['sharelist'][designatedLocation]
    content['number'] -= 1
    await Utils.writeTo(p, content)
    return ok


async def deleteSpecifiedFollower(userQQ, followQQ):
    user = await Utils.userInformationQuery(userQQ)
    if user == error:
        raise GrailExcept
    entourage = user['entourage']
    cleanEntourage = []
    for e in entourage['follower_information']:
        if e['qq'] != followQQ:
            cleanEntourage.append(e)
    entourage['number'] -= 1
    entourage['follower_information'] = cleanEntourage
    user['entourage'] = entourage
    await Utils.writeUserInformation(userQQ, user)
    # Clean up the pool
    await cleanUpTheRecordPool(userQQ, followQQ)
    await deleteSharePool(userQQ, followQQ)
    return ok


async def releaseAttendants(userQQ, followQQ):
    msg = await Utils.atQQ(userQQ)
    followInfo = await Utils3.getTheSpecifiedFollowerInformation(userQQ, followQQ)
    if followInfo != 0:
        # Start deletion
        await deleteSpecifiedFollower(userQQ, followQQ)
        msg += '你无情地抛弃了「' + followInfo['name'] + '」。'
        return msg
    return error


async def detailsOfTheAttendant(userQQ, followQQ):
    msg = await Utils.atQQ(userQQ)
    follow = await Utils3.getTheSpecifiedFollowerInformation(userQQ, followQQ)
    if follow != 0:
        status = await updateAllSharedData(userQQ)
        if status == error:
            return error
        follow = await Utils3.getTheSpecifiedFollowerInformation(userQQ, followQQ)
        if follow['combat_effectiveness']['ranking'] > 200:
            follow['combat_effectiveness']['ranking'] == '千里之外'
        timeToGetAlong = await initialization.timeDifferenceFromNowOn(follow['arrest_time']['arrest_time'])
        msg += (
            '和 Master 在一起' + str(timeToGetAlong + 1) + '天啦' + '\n\n'
            '名称：' + follow['name'] + '(' + str(follow['qq']) + ')' + '\n' + 
            '战斗力：' + str(follow['combat_effectiveness']['initial_fighting_power']) + '\n' +
            '    - 基础：+' + str(follow['combat_effectiveness']['basics']) + '\n' +
            '    - 技能加成：+' + str(follow['combat_effectiveness']['skill']['total_combat_strength']) + '\n' +
            '(' + follow['combat_effectiveness']['skill']['quality']['name'] + 
            '+' + str(follow['combat_effectiveness']['skill']['quality']['combat_effectiveness']) + 
            ')\n' + '    - 共享加成：+' + str(follow['combat_effectiveness']['shared_combat_effectiveness']) +
            '（动态更新）\n' + '全服排名：' + str(follow['combat_effectiveness']['ranking']) + '\n\n'
            '【技能】\n' + follow['combat_effectiveness']['skill']['name'] + 
            follow['combat_effectiveness']['skill']['quality']['name'] + '：' + 
            follow['combat_effectiveness']['skill']['introduce'] + '\n\n' + '目前有 ' + 
            str(follow['combat_effectiveness']['share_number']) + ' 位 Master 共同享有 ' + 
            follow['name']
        )
        return msg
    return error


async def basicCombatCapability(userQQ):
    knapsack = await Utils3.getTheContentsOfUserIsBackpackUnit(userQQ)
    basicCombat = 100
    for k in knapsack:
        if k['id'] == 3:
            basicCombat += k['number']
    return basicCombat
    
    

async def obtainAllTheFollowingForcesOfUsers(userQQ):
    combatEffectiveness = 0
    follows = await Utils3.getInformationOfUserSFollowerModule(userQQ)
    if follows['number'] == 0:
        return 0
    for f in follows['follower_information']:
        combatEffectiveness += f['combat_effectiveness']['initial_fighting_power']
    return combatEffectiveness


async def statisticsOfSingleCombatPower(userQQ, id):
    combatEffectiveness = 0
    combatEffectiveness += await basicCombatCapability(userQQ)
    combatEffectiveness += await obtainAllTheFollowingForcesOfUsers(userQQ)
    if id != 0:
        goodsInfo = await Utils.getItemInformation(id)
        if goodsInfo == error:
            raise GrailExcept
        selectedForces = random.randint(goodsInfo['lower_limit_of_combat_power'],
                                            goodsInfo['upper_limit_of_war_power'])
        combatEffectiveness += selectedForces
    return combatEffectiveness


async def judgeTheBattle(userQQ, targetQQ, id):
    userQQCombatEffectiveness = await statisticsOfSingleCombatPower(userQQ, id)
    targetQQCombatEffectiveness = await statisticsOfSingleCombatPower(userQQ, 0)
    if userQQCombatEffectiveness >= targetQQCombatEffectiveness:
        return 1
    return 0


async def extractBattleResultMessageSegment(winnerQQ, loserQQ):
    winner = await Utils.userInformationQuery(winnerQQ)
    loser = await Utils.userInformationQuery(loserQQ)
    if winner == error or loser == error:
        raise GrailExcept
    p = './HolyGrailWar/Config/Battle/Plot.json'
    content = await Utils.readFileToJSON(p)
    if content == error:
        raise GrailExcept
    selectedStory = random.choice(content['plotlist'])
    selectedStory = selectedStory['content'].replace(r'{winner}',
                    winner['register']['register_group_business_card']).replace(r'{loser}',
                    loser['register']['register_group_business_card'])
    return selectedStory


async def getGroupBusinessCardWhenUsersRegister(userQQ):
    user = await Utils.userInformationQuery(userQQ)
    if user == error:
        raise GrailExcept
    return user['register']['register_group_business_card']


async def battleSettlementGrainAndGoldCoin(winnerQQ, loserQQ):
    foodstuff = random.randint(50,200)
    gold = random.randint(50,200)
    deductionOfGoldCoins = random.randint(50,100)
    # Settlement
    await Utils.additionAndSubtractionOfUserInformationData(winnerQQ, 'resources', 'foodstuff', 
                                                                                    foodstuff)
    await Utils.rigidGoldCoinAdditionAndSubtraction(winnerQQ, gold)
    await Utils.rigidGoldCoinAdditionAndSubtraction(loserQQ, (-1)*gold)
    return [foodstuff,gold,deductionOfGoldCoins]
    

async def updateCombatTimes(winnerQQ, loserQQ):
    winner = await Utils.userInformationQuery(winnerQQ)
    loser = await Utils.userInformationQuery(loserQQ)
    if winner == error or loser == error:
        raise GrailExcept
    nowTime = await initialization.getCurrentDate()
    # winner
    winner['battle']['frequency'] += 1
    winner['battle']['victory'] += 1
    if nowTime == winner['battle']['last_battle_time']:
        winner['battle']['number_of_battles_of_the_day'] += 1
    else:
        winner['battle']['number_of_battles_of_the_day'] = 1
    winner['battle']['last_battle_time'] = nowTime
    winnerWinningProbability = float(winner['battle']['victory']) / float(winner['battle']['frequency'])
    # loser
    loser['battle']['frequency'] += 1
    loser['battle']['fail'] += 1
    loserWinningProbability = float(loser['battle']['victory']) / float(loser['battle']['frequency'])
    # Write in
    await Utils.writeUserInformation(winnerQQ, winner)
    await Utils.writeUserInformation(loserQQ, loser)
    return [winner['battle']['frequency'], winnerWinningProbability,winner['battle']['number_of_battles_of_the_day'],
            loser['battle']['frequency'], loserWinningProbability]


async def getAccurateTime():
    nowDate = str(datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d/%H:%M:%S'))
    return nowDate


async def judgeTimeDifference(lastTime):
    timeNow = await getAccurateTime()
    a = parse(lastTime)
    b = parse(timeNow)
    return int((b - a).total_seconds())


async def judgeAttackCd(userQQ):
    nowTimeAbbreviation = await initialization.getCurrentDate()
    p = './HolyGrailWar/User/Battle/CombatRecord_' + str(nowTimeAbbreviation) + '.json'
    content = await Utils.readFileToJSON(p)
    nowTimeAbbreviation = await getAccurateTime()
    if content == error:
        FileStructure = {
            "recordlist": []
        }
        await Utils.writeTo(p, FileStructure)
        content = await Utils.readFileToJSON(p)
    for c in content['recordlist']:
        if c['qq'] == userQQ:
            timeDifference = await judgeTimeDifference(c['time'])
            if timeDifference >= 180:
                return ok
            else:
                return 180 - timeDifference
    return ok


async def performingBattleRecords(userQQ):
    nowTimeAbbreviation = await initialization.getCurrentDate()
    p = './HolyGrailWar/User/Battle/CombatRecord_' + str(nowTimeAbbreviation) + '.json'
    content = await Utils.readFileToJSON(p)
    nowTimeAbbreviation = await getAccurateTime()
    if content == error:
        raise GrailExcept
    mark = 0
    for c in content['recordlist']:
        if c['qq'] == userQQ:
            c['time'] = nowTimeAbbreviation
            mark = 1
            break
    if mark == 0:
        userBattleRecordStructure = {
            "qq": userQQ,
            "time": nowTimeAbbreviation
        }
        content['recordlist'].append(userBattleRecordStructure)
    # Write in
    await Utils.writeTo(p, content)
    return ok


async def checkWhetherThereAreAttackProps(userQQ):
    knapsack = await Utils3.getTheContentsOfUserIsBackpackUnit(userQQ)
    if knapsack == []:
        return 0
    listOfProps = []
    combatableItemsList = [3, 4, 6, 12]
    for k in knapsack:
        if k['id'] in combatableItemsList:
            listOfProps.append(k)
    # Adding combat power
    for l in listOfProps:
        l['item_details'] = await Utils.getItemInformation(l['id'])
    return listOfProps


async def automaticSelectionOfCombatItems(userQQ):
    listOfProps = await checkWhetherThereAreAttackProps(userQQ)
    prop = random.choice(listOfProps)
    # Deduction of props
    await Utils2.deductionOfGoods(userQQ, prop['id'], 1)
    return prop['id']


async def getTheNumberOfAttacksOfTheDayByTheUser(userQQ):
    user = await Utils.userInformationQuery(userQQ)
    if user == error:
        raise GrailExcept
    nowTime = await initialization.getCurrentDate()
    if user['battle']['last_battle_time'] != nowTime:
        return 0
    return user['battle']['number_of_battles_of_the_day']


async def seeIfThereIsACombatPermit(userQQ):
    knapsack = await Utils3.getTheContentsOfUserIsBackpackUnit(userQQ)
    if knapsack == []:
        return error
    for k in knapsack:
        if k['id'] == 11:
            return 1
    return error


async def constructWinningMessageSegment(userQQ, targetQQ, id, model = 'one_click_attack'):
    msg = ''
    battleToWinOrLose = await judgeTheBattle(userQQ, targetQQ, id)
    if model == 'one_click_attack':
        msg += '⚡ 一键攻击模式，随机使用了背包中的武器 '
        # Weapon extraction
        id = await automaticSelectionOfCombatItems(userQQ)
        goodsInfo = await Utils.getItemInformation(id)
        msg += '[' + goodsInfo['name'] + 'x1]\n\n'
    else:
        msg += '⚔ 已选择「'
        goodsInfo = await Utils.getItemInformation(id)
        msg += goodsInfo['name'] + '」作为武器\n\n'
        # Deduction of props
        await Utils2.deductionOfGoods(userQQ, id, 1)
    msg += '战斗结果：\n'
    if battleToWinOrLose == 1:
        winnerQQ, loserQQ = userQQ, targetQQ
    else:
        winnerQQ, loserQQ = targetQQ, userQQ
    msg += await extractBattleResultMessageSegment(winnerQQ, loserQQ)
    settlementResult = await battleSettlementGrainAndGoldCoin(winnerQQ, loserQQ)
    combatRecordResults = await updateCombatTimes(winnerQQ, loserQQ)
    msg += ('\n\n' + '【胜利】' + await getGroupBusinessCardWhenUsersRegister(winnerQQ) + 
            '（+' + str(settlementResult[0]) + '粮食，+' + 
            str(settlementResult[1]) + '金币）\n' + 
            '   - 战斗次数:' + str(combatRecordResults[0]) + '\n' +
            '    - 胜率：' + str( round(100 * combatRecordResults[1], 1) ) + '%\n\n' + 
            '【失败】' + await getGroupBusinessCardWhenUsersRegister(loserQQ) + 
            '（-' + str(settlementResult[2]) + '金币）\n' + 
            '   - 战斗次数:' + str(combatRecordResults[3]) + '\n' +
            '    - 胜率：' + str( round(100 * combatRecordResults[4], 1) ) + '%\n\n' + 
            '当天已用战斗次数(' + 
            str(combatRecordResults[2]) + '/10)')
    # Combat record of the day
    await performingBattleRecords(userQQ)
    return msg


async def determineIfAOneClickAttackIsPossible(userQQ, targetQQ,  model = 'one_click_attack'):
    msg = await Utils.atQQ(userQQ)
    # Judge whether the opponent is registered
    target = await Utils.userInformationQuery(targetQQ)
    if target == error:
        msg += '你选择的对手不存在或未注册为 Master.\n注：对方至少要执行一次「探险」或「捕捉」来参加圣杯战争。'
        return msg
    # Determine the number of attacks on that day
    numberOfAttacks = await getTheNumberOfAttacksOfTheDayByTheUser(userQQ)
    if numberOfAttacks >= 10:
        msg += '今天战斗次数已达上限(10/10)'
        return msg
    # Judge how long the last battle has lasted
    status = await judgeAttackCd(userQQ)
    if status != ok:
        msg += '每次「攻击」至少需要间隔180秒，你还需要等待' + str(status) + '秒才能进行下一次攻击。'
        return msg
    # Judge whether there is a combat permit
    combatPermit = await seeIfThereIsACombatPermit(userQQ)
    if combatPermit == error:
        msg += '你目前没有战斗许可证，发起攻击至少需要一个战斗许可证\n*注：[战斗许可证] 可从「商店」进行购买。'
        return msg
    # Judge whether there are weapons to fight
    listOfProps = await checkWhetherThereAreAttackProps(userQQ)
    if listOfProps == []:
        msg += '没有可以战斗的武器哦。'
        return msg
    # Deduct combat permit
    await Utils2.deductionOfGoods(userQQ, 11, 1)
    msg += await constructWinningMessageSegment(userQQ, targetQQ, 0, model)
    return msg


async def addSingleStepCombatToken(userQQ, targetQQ, goodsList):
    p = './HolyGrailWar/User/Battle/Battle.json'
    content = await Utils.readFileToJSON(p)
    if content == error:
        battleFileStructure = {
            "battlelist": [],
            "number": 0
        }
        await Utils.writeTo(p, battleFileStructure)
        content = await Utils.readFileToJSON(p)
    nowTime = await getAccurateTime()
    userBattleStructure = {
        "qq": userQQ,
        "target": targetQQ,
        "time": nowTime,
        "goods_list": goodsList
    }
    content['battlelist'].append(userBattleStructure)
    content['number'] += 1
    await Utils.writeTo(p, content)
    return ok


async def checkWhetherThereIsABattleMark(userQQ):
    p = './HolyGrailWar/User/Battle/Battle.json'
    content = await Utils.readFileToJSON(p)
    if content == error:
        return error
    if content['number'] == 0:
        return 0
    for c in content['battlelist']:
        if c['qq'] == userQQ:
            return c
    return 0


async def removeBattleMarks(userQQ):
    p = './HolyGrailWar/User/Battle/Battle.json'
    content = await Utils.readFileToJSON(p)
    if content == error:
        raise GrailExcept
    weedingPosition = 0
    for index,value in enumerate(content['battlelist']):
        if value['qq'] == userQQ:
            weedingPosition = index
            break
    del content['battlelist'][weedingPosition]
    content['number'] -= 1
    await Utils.writeTo(p, content)
    return ok


async def theSecondStepOfSingleCombat(userQQ):
    # Check whether there is a battle mark
    status = await checkWhetherThereIsABattleMark(userQQ)
    if status != error and status != 0:
        # Judge time difference
        timeDifference = await judgeTimeDifference(status['time'])
        # Remove battle marks
        await removeBattleMarks(userQQ)
        if timeDifference <= 30:
            # Not expired
            return status
    return 0


async def singleStepAttack(status, id):
    # Direct execution
    msg = await Utils.atQQ(status['qq'])
    msg += await constructWinningMessageSegment(status['qq'], status['target'],
                                                status['goods_list'][int(id) - 1]['id'], 'single_step')
    return msg


async def isItPossibleToPerformASingleAttack(userQQ, targetQQ):
    msg = await Utils.atQQ(userQQ)
    # Judge whether the opponent is registered
    target = await Utils.userInformationQuery(targetQQ)
    if target == error:
        msg += '你选择的对手不存在或未注册为 Master.\n注：对方至少要执行一次「探险」或「捕捉」来参加圣杯战争。'
        return msg
    # Determine the number of attacks on that day
    numberOfAttacks = await getTheNumberOfAttacksOfTheDayByTheUser(userQQ)
    if numberOfAttacks >= 10:
        msg += '今天战斗次数已达上限(10/10)'
        return msg
    # Judge how long the last battle has lasted
    status = await judgeAttackCd(userQQ)
    if status != ok:
        msg += '每次「攻击」至少需要间隔180秒，你还需要等待' + str(status) + '秒才能进行下一次攻击。'
        return msg
    # Judge whether there is a combat permit
    combatPermit = await seeIfThereIsACombatPermit(userQQ)
    if combatPermit == error:
        msg += '你目前没有战斗许可证，发起攻击至少需要一个战斗许可证\n*注：[战斗许可证] 可从「商店」进行购买。'
        return msg
    # Judge whether there are weapons to fight
    listOfProps = await checkWhetherThereAreAttackProps(userQQ)
    if listOfProps == []:
        msg += '没有可以战斗的武器哦。'
        return msg
    # Deduct combat permit
    await Utils2.deductionOfGoods(userQQ, 11, 1)
    msg += ('准备向' + target['register']['register_group_business_card'] + 
            '发起攻击，为战斗选择一件趁手的装备获得战斗力加成！\n' + 
            '以下是你的背包中已有装备：\n')
    for index,l in enumerate(listOfProps):
        msg += ('[' + str(index + 1) + '] ' + l['item_details']['name'] + ' x ' + 
                str(l['number']) + '\n' + '  - ' + l['item_details']['introduce'] + '\n' +
                '  - ' + '战斗力：' + str(l['item_details']['lower_limit_of_combat_power']) + 
                '~' + str(l['item_details']['upper_limit_of_war_power']) + '\n' )
    msg += '\n' + '*输入序号进行选择。请在30秒内完成选择，否则此次攻击请求自动取消。'
    # Add single step combat token
    await addSingleStepCombatToken(userQQ, targetQQ, listOfProps)
    return msg









# -*- coding: utf-8 -*-

import os
import ujson
import random
import aiofiles
from . import Utils
from . import Utils2
from . import initialization
from .customException import GrailExcept

error = 'error'
ok = 'ok'

async def helpMenu(userQQ):
    p = './HolyGrailWar/Config/UserAssistance/help.json'
    msg = ''
    content = await Utils.readFileToJSON(p)
    if content == error:
        raise GrailExcept
    msg += (content['prefix'] + '\n\n' + content['follower_function'] + '\n\n' + 
                content['combat_function'] + '\n\n' + content['adventure_function'] + '\n\n' + 
                content['store_function'] + '\n\n' + content['leaderboard_function'])
    return msg


async def customParameterReading(fieldName):
    p = './HolyGrailWar/Config/Custom/CustomParameters.json'
    content = await Utils.readFileToJSON(p)
    if content == error:
        raise GrailExcept
    if str(fieldName) not in content:
        return error
    return content[str(fieldName)]


async def initializationOfBasicCombatPower():
    p = './HolyGrailWar/Config/Custom/CustomParameters.json'
    content = await Utils.readFileToJSON(p)
    if content == error:
        raise GrailExcept
    if 'possible_maximum_of_basic_combat_power' not in content:
        raise GrailExcept
    if 'possible_minimum_of_basic_combat_power' not in content:
        raise GrailExcept
    chooseRandomForces = random.randint(int(content['possible_minimum_of_basic_combat_power']),
                                        int(content['possible_maximum_of_basic_combat_power']))
    return int(chooseRandomForces)


async def extractQualityUnit():
    p = './HolyGrailWar/Config/Skill/Quality.json'
    content = await Utils.readFileToJSON(p)
    if content == error:
        raise GrailExcept
    selectedNumber = random.randint(1,100)
    for q in content['qualitylist']:
        if q['range'][1] >= selectedNumber and q['range'][0] <= selectedNumber:
            # Meeting conditions
            extractTheCorrespondingQualityValue = random.randint(q['lower_limit_of_additional_combat_power'],
                                                                q['additional_maximum_combat_power'])
            # Construct quality unit
            qualityUnit = {
                "id": q['id'],
                "name": q['name'],
                "combat_effectiveness": int(extractTheCorrespondingQualityValue)
            }
            return qualityUnit
    return error

async def skillAddedQuality(skill):
    # Add quality unit
    skill['quality'] = await extractQualityUnit()
    if skill['quality'] == error:
        raise GrailExcept
    return skill


async def extractSkillsFromWarehouse():
    p = './HolyGrailWar/Config/Skill/SkillDepository.json'
    content = await Utils.readFileToJSON(p)
    if content == error:
        raise GrailExcept
    listOfNonSpecialSkills = []
    for s in content['skilllist']:
        if 'special' not in s:
            listOfNonSpecialSkills.append(s)
    skillsExtracted = random.choice(listOfNonSpecialSkills)
    skillsExtracted['combat_strength'] = random.randint(skillsExtracted['minimum_combat_strength'],
                                                        skillsExtracted['maximum_combat_strength'])
    # Start to add quality
    skillsExtracted = await skillAddedQuality(skillsExtracted)
    skillsExtracted['total_combat_strength'] = skillsExtracted['quality']['combat_effectiveness'] + skillsExtracted['combat_strength']
    # Rebound add quality skills
    return skillsExtracted


async def getTheNumberOfShares(followQQ):
    p = './HolyGrailWar/User/Servant/SharePool.json'
    content = await Utils.readFileToJSON(p)
    if content == error:
        raise GrailExcept
    number = 0
    for s in content['sharelist']:
        if s['follow_qq'] == followQQ:
            number += 1
    return number


async def computingSharedForces(followQQ, model = 'default'):
    number = await getTheNumberOfShares(followQQ)
    decrement = await customParameterReading('decrement_parameter')
    minimumValue = await customParameterReading('minimum_reduction_ratio')
    numberOfPeople = await customParameterReading('starting_number_of_people_to_decline')
    if number >= numberOfPeople:
        if (100 - number * decrement) < minimumValue:
            number = number * minimumValue / 100
            if model != 'default':
                return (1 - minimumValue / 100) * 100
        else:
            number = number * (1 - number * decrement / 100)
            if model != 'default':
                return (1 - (1 - number * decrement / 100)) * 100
    return int(number)
    

async def addToRecordPool(followInfo):
    recordPoolStructure = {
        "recordlist":[],
        "number": 0
    }
    p = './HolyGrailWar/User/Servant/RecordPool.json'
    content = await Utils.readFileToJSON(p)
    if content == error:
        # Create a shared pool
        await Utils.writeTo(p, recordPoolStructure)
        content = await Utils.readFileToJSON(p)
    content['recordlist'].append(followInfo)
    content['number'] += 1
    # Write in
    await Utils.writeTo(p, content)
    return ok


async def refreshRecordPoolRanking(userQQ, followQQ):
    p = './HolyGrailWar/User/Servant/RecordPool.json'
    content = await Utils.readFileToJSON(p)
    if content == error:
        raise GrailExcept
    followList = content['recordlist']
    followList.sort(key = lambda x:x['combat_effectiveness']['initial_fighting_power'], reverse = True)
    number = 0
    for f in followList:
        number += 1
        if f['master'] == userQQ and f['qq'] == followQQ:
            return number
            

async def registeredAttendant(bot, followerQQ, followerGroup, userQQ):
    # Start registration does not exist
    pTemplate = './HolyGrailWar/Config/Register/FollowerTemplate.json'
    registrationTemplate = await Utils.readFileToJSON(pTemplate)
    if registrationTemplate == error:
        raise GrailExcept
    # Refresh registration information
    registrationTemplate['master'] = userQQ
    registrationTemplate['qq'] = followerQQ
    registrationTemplate['name'] = await Utils.takeTheNameOfThePerson(bot, followerQQ, followerGroup)
    arrestTime = registrationTemplate['arrest_time']
    arrestTime['business_cards_in_capture'] = registrationTemplate['name']
    arrestTime['nickname_for_capture'] = await Utils.getUserNickname(bot, followerQQ, followerGroup)
    arrestTime['arrest_time'] = await initialization.getCurrentDate()
    arrestTime['catch_group'] = followerGroup
    arrestTime['capture_group_code'] = await initialization.getOrWriteNumber(userQQ, 
                                                                    followerGroup, 'group')
    registrationTemplate['arrest_time'] = arrestTime
    # Combat effectiveness initialization
    combatEffectiveness = registrationTemplate['combat_effectiveness']
    combatEffectiveness['basics'] = await initializationOfBasicCombatPower()
    combatEffectiveness['skill'] = await extractSkillsFromWarehouse()
    combatEffectiveness['shared_combat_effectiveness'] = await computingSharedForces(followerQQ)
    combatEffectiveness['share_number'] = await getTheNumberOfShares(followerQQ)
    combatEffectiveness['initial_fighting_power'] = combatEffectiveness['basics'] + combatEffectiveness['skill']['total_combat_strength']
    registrationTemplate['combat_effectiveness'] = combatEffectiveness
    return registrationTemplate


async def captureSuccessfullyAddedToYourOwnLibrary(bot, userQQ, followerQQ, followerGroup):
    user = await Utils.userInformationQuery(userQQ)
    if user == error:
        raise GrailExcept
    generateFollowerObject = await registeredAttendant(bot, followerQQ, followerGroup, userQQ)
    # Write to record pool
    await addToRecordPool(generateFollowerObject)
    generateFollowerObject['combat_effectiveness']['ranking'] = await refreshRecordPoolRanking(userQQ, followerQQ)
    user['entourage']['number'] += 1
    user['entourage']['follower_information'].append(generateFollowerObject)
    # Write back
    status = await Utils.writeUserInformation(userQQ, user)
    if status == error:
        return error
    return generateFollowerObject


async def checkWhetherThereIsAPropForRaisingTheUpperLimit(userQQ):
    user = await Utils.userInformationQuery(userQQ)
    if user == error:
        return error
    knapsack = user['knapsack']
    for k in knapsack:
        # Grail fragments
        if k['id'] == 16:
            return int(k['number'])
    return 0


async def judgeWhetherToBeArrested(userQQ, followQQ, model = 'default'):
    user = await Utils.userInformationQuery(userQQ)
    if user == error:
        return error
    followerInformation = user['entourage']
    number = followerInformation['number']
    entourage = followerInformation['follower_information']
    # already expired
    maxNumber = 3
    numberPlus = await checkWhetherThereIsAPropForRaisingTheUpperLimit(userQQ)
    if numberPlus == error:
        raise GrailExcept
    if numberPlus > 0:
        maxNumber += numberPlus
    if model != 'default':
        return maxNumber
    if number >= maxNumber:
        return 1
    # existence
    for e in entourage:
        if e['qq'] == followQQ:
            return 2
    return ok


async def getTheCurrentNumberOfFollowers(userQQ):
    user = await Utils.userInformationQuery(userQQ)
    if user == error:
        raise GrailExcept
    return str(user['entourage']['number'])


async def getInformationOfUserSFollowerModule(userQQ):
    user = await Utils.userInformationQuery(userQQ)
    if user == error:
        raise GrailExcept
    return user['entourage']


async def getTheSpecifiedFollowerInformation(userQQ, followQQ):
    entourage = await getInformationOfUserSFollowerModule(userQQ)
    number = entourage['number']
    followerInformation = entourage['follower_information']
    if number == 0:
        return 0
    for f in followerInformation:
        if f['qq'] == followQQ:
            return f
    return 0


async def getTheContentsOfUserIsBackpackUnit(userQQ):
    user = await Utils.userInformationQuery(userQQ)
    if user == error:
        raise GrailExcept
    return user['knapsack']
    

async def getTheFirstMessageOfCaptureResultOrFailure(id, model = 'success'):
    p = './HolyGrailWar/Config/Catch/information.json'
    content = await Utils.readFileToJSON(p)
    if content == error:
        raise GrailExcept
    if model == 'success':
        msgList = content['catchlist']
        for m in msgList:
            if m['goodsid'] == id:
                return m['msg']
    else:
        msgList = content['notcatch']
        for m in msgList:
            if m['goodsid'] == id:
                return m['msg']


async def captureSuccessProbability(bot, userQQ, followQQ, userGroup):
    # Random number method 
    # Items tested
    knapsack = await getTheContentsOfUserIsBackpackUnit(userQQ)
    mark = 0
    for k in knapsack:
        # Advanced master ball
        if k['id'] == 2:
            mark = 2
            break
        # Lethargic black tea
        if k['id'] == 12:
            mark = 12
            break
        # Master ball
        if k['id'] == 1:
            mark = 1
            break
    markSuccessOrNot = 0
    if mark == 0:
        # No props
        msg = await getTheFirstMessageOfCaptureResultOrFailure(0, model = 'fail')
    if mark == 1:
        probability = random.randint(1, 100)
        if probability >= 30: 
            msg = await getTheFirstMessageOfCaptureResultOrFailure(1, model = 'success')
            markSuccessOrNot = 1
        else:
            msg = await getTheFirstMessageOfCaptureResultOrFailure(1, model = 'fail')
    if mark == 2:
        msg = await getTheFirstMessageOfCaptureResultOrFailure(2, model = 'success')
        markSuccessOrNot = 1
    if mark == 12:
        probability = random.randint(1, 100)
        if probability >= 15: 
            msg = await getTheFirstMessageOfCaptureResultOrFailure(12, model = 'success')
            markSuccessOrNot = 1
        else:
            msg = await getTheFirstMessageOfCaptureResultOrFailure(12, model = 'fail')
    # Replace message content
    userName = await Utils.takeTheNameOfThePerson(bot, userQQ, userGroup)
    followName = await Utils.takeTheNameOfThePerson(bot, followQQ, userGroup)
    msg = msg.replace(r'{master}', str(userName)).replace(r'{follow}', str(followName))
    return [markSuccessOrNot, msg, mark]


async def addToSharedPool(userQQ, followQQ):
    sharedPoolStructure = {
        "sharelist":[],
        "number": 0
    }
    p = './HolyGrailWar/User/Servant/SharePool.json'
    content = await Utils.readFileToJSON(p)
    if content == error:
        # Create a shared pool
        await Utils.writeTo(p, sharedPoolStructure)
        content = await Utils.readFileToJSON(p)
    userStructure = {
        "qq": userQQ,
        "follow_qq": followQQ,
        "time": "2017-10-01"
    }
    userStructure['time'] = await initialization.getCurrentDate()
    content['sharelist'].append(userStructure)
    content['number'] += 1
    # Write in
    await Utils.writeTo(p, content)
    return ok


async def generateFollowerFirstLevelProcessing(userQQ, followQQ):
    # Add to share pool
    await addToSharedPool(userQQ, followQQ)


async def captureTheFirstLevelOfTreatment(bot, userQQ, followQQ, followGroup):
    msg = await Utils.atQQ(userQQ)
    # Judge whether the arrested person is registered
    followUser = await Utils.userInformationQuery(followQQ)
    if followUser == error:
        msg += '你选择的对手不存在或未注册为 Master.\n注：对方至少要执行一次「探险」或「捕捉」来参加圣杯战争。'
        return msg
    # Judge whether the catcher can catch
    status = await judgeWhetherToBeArrested(userQQ, followQQ)
    if status == error:
        return error
    if status == 1:
        # The attendant is full.
        msg += '你已经拥有'       
        msg += await getTheCurrentNumberOfFollowers(userQQ)
        msg += '个随从了，没办法再添加更多的随从了呢。可以通过道具来提升携带的随从数，或放生随从一个来腾出位置。'
        return msg
    elif status == 2:
        # The follower already exists
        statusFollow = await getTheSpecifiedFollowerInformation(userQQ, followQQ)
        if statusFollow != 0:
            # existence
            msg += statusFollow['name'] + '已经是你的 Servant 了。'
            return msg
        raise GrailExcept
    # Can catch
    else:
        # Obtain the probability of successful capture
        previousMessage = await captureSuccessProbability(bot, userQQ, followQQ, followGroup)
        if previousMessage[0] == 0:
            previousMessage[1] = msg + previousMessage[1]
            # Operating items
            goodsNumber = await Utils2.deductionOfGoods(userQQ, previousMessage[2], 1)
            # fail
            return previousMessage
        else:
            # Success
            # Enter the registration process
            await generateFollowerFirstLevelProcessing(userQQ, followQQ)
            generateFollowerObject = await captureSuccessfullyAddedToYourOwnLibrary(bot, userQQ, followQQ, followGroup)
            # Message structure
            previousMessage[1] = msg + '【捕捉】' + previousMessage[1]
            msg += ('【捕捉成功】' + generateFollowerObject['name'] + '已成为你的 Servant：\n\n' +
                    '名称：' + generateFollowerObject['name'] + '(' + str(generateFollowerObject['qq']) + 
                    ')\n' + '战斗力：' + 
                    str(int(generateFollowerObject['combat_effectiveness']['initial_fighting_power'])
                     + int(generateFollowerObject['combat_effectiveness']['shared_combat_effectiveness'])) + 
                    '\n' + '    - 基础：+' + 
                    str(generateFollowerObject['combat_effectiveness']['basics']) + 
                    '\n' + '    - 技能加成：+' + 
                    str(generateFollowerObject['combat_effectiveness']['skill']['total_combat_strength']) +
                    '(' + generateFollowerObject['combat_effectiveness']['skill']['quality']['name'] + 
                    '+' + str(generateFollowerObject['combat_effectiveness']['skill']['quality']['combat_effectiveness']) + 
                    ')\n' + '    - 共享加成：+' + 
                    str(generateFollowerObject['combat_effectiveness']['shared_combat_effectiveness']) +
                    '（动态更新）\n\n' + '【技能】\n' + 
                    generateFollowerObject['combat_effectiveness']['skill']['name'] + 
                    generateFollowerObject['combat_effectiveness']['skill']['quality']['name'] +
                    '：' + generateFollowerObject['combat_effectiveness']['skill']['introduce'] + 
                    '\n\n' + '目前有 ' + 
                    str(generateFollowerObject['combat_effectiveness']['share_number']) +
                    ' 位 Master 共同享有 ' + generateFollowerObject['name'] + '\n\n' + 
                    '剩余')
            goodsInfo = await Utils.getItemInformation(previousMessage[2])
            # Operating items
            goodsNumber = await Utils2.deductionOfGoods(userQQ, previousMessage[2], 1)
            msg += (goodsInfo['name'] + '：' + str(goodsNumber))
            previousMessage.append(msg)
            return previousMessage



            

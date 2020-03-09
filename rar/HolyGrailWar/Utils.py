# -*- coding: utf-8 -*-

import os
import random
import aiofiles
import ujson
from . import Utils2plus
from .customException import GrailExcept

# Non fatal error type
error = 'error'
ok = 'ok'
insufficient = 'insufficient'

async def takeTheNameOfThePerson(bot, userQQ, userGroup):
    nickname = '您'
    try:
        info = await bot.get_group_member_info(user_id = int(userQQ), group_id = int(userGroup),
                                                    no_cache = True)
        nickname = info['card']
        if nickname == '':
            nickname = info['nickname']
            if nickname == '':
                nickname = ' '
    except:
        pass
    return nickname


async def getUserNickname(bot, userQQ, userGroup):
    nickname = '您'
    try:
        info = await bot.get_group_member_info(user_id = int(userQQ), group_id = int(userGroup),
                                                    no_cache = True)
        nickname = info['nickname']
        if nickname == '':
            nickname = ' '
    except:
        pass
    return nickname


async def atQQ(userQQ):
    return '[CQ:at,qq=' + str(userQQ) + ']\n'


async def readFileToJSON(p):
    if not os.path.exists(p):
        return error
    async with aiofiles.open(p, 'r', encoding='utf-8') as f:
        content = await f.read()
    content = ujson.loads(content)
    return content


async def writeTo(p, info):
    async with aiofiles.open(p, 'w', encoding='utf-8') as f:
        await f.write(ujson.dumps(info))
    return ok
    

async def getItemInformation(id):
    p = './HolyGrailWar/Config/Goods/Goods.json'
    content = await readFileToJSON(p)
    if content == error:
        raise GrailExcept
    if 'goodslist' not in content:
        raise GrailExcept
    goodsList = content['goodslist']
    for g in goodsList:
        if int(id) == g['id']:
            return g
    return error


async def userInformationQuery(userQQ):
    p = './HolyGrailWar/User/Data/' + str(userQQ) + '.json'
    if not os.path.exists(p):
        return error
    async with aiofiles.open(p, 'r', encoding='utf-8') as f:
        content = await f.read()
    content = ujson.loads(content)
    return content
    

async def getUserRemainingResources(userQQ):
    user = await userInformationQuery(int(userQQ))
    if user == error:
        raise GrailExcept
    resources = user['resources']
    msg = '剩余粮食：' + str( resources['foodstuff'] ) + '，金币：' + str( resources['gold'] )
    return msg


async def writeUserInformation(userQQ, info):
    p = './HolyGrailWar/User/Data/' + str(userQQ) + '.json'
    if not os.path.exists(p):
        return error
    async with aiofiles.open(p, 'w', encoding='utf-8') as f:
        info = ujson.dumps(info)
        await f.write(info)
    return ok


async def generalUserInformationOperation(userQQ, classification, field, afterOperation):
    user = await userInformationQuery(userQQ)
    if user == error:
        raise GrailExcept
    # Native
    if classification == 'native':
        user[field] = afterOperation
    else:
        if classification not in user:
            raise GrailExcept
        if field not in user[classification]:
            raise GrailExcept
        user[classification][field] = afterOperation
    # Write information
    status = await writeUserInformation(userQQ, user)
    if status == ok:
        return ok
    return error
        

async def additionAndSubtractionOfUserInformationData(userQQ, classification, field, operationValue):
    user = await userInformationQuery(userQQ)
    if user == error:
        raise GrailExcept
    # Native
    if classification == 'native':
        surplus = user[field] + operationValue
        if  surplus >= 0:
            user[field] += operationValue
        else:
            return insufficient + ' ' + str(user[field])
    else:
        if classification not in user:
            raise GrailExcept
        if field not in user[classification]:
            raise GrailExcept
        surplus = user[classification][field] + operationValue
        if surplus >= 0:
            user[classification][field] += operationValue
        else:
            return insufficient + ' ' + str(user[classification][field])
    # Write information
    status = await writeUserInformation(userQQ, user)
    if status == error:
        return error
    return surplus
            

async def rigidGoldCoinAdditionAndSubtraction(userQQ, operationValue):
    user = await userInformationQuery(userQQ)
    if user == error:
        raise GrailExcept
    gold = user['resources']['gold']
    user['resources']['gold'] += operationValue
    surplus = user['resources']['gold']
    # Write information
    status = await writeUserInformation(userQQ, user)
    if status == error:
        return error
    return surplus


async def addItems(userQQ, itemNumber, number):
    user = await userInformationQuery(userQQ)
    if user == error:
        raise GrailExcept
    knapsack = user['knapsack']
    existence = 0
    for k in knapsack:
        if k['id'] == itemNumber:
            k['number'] += number
            existence = 1
            break
    if existence == 0:
        goods = {
            "id": int(itemNumber),
            "number": int(number)
        }
        knapsack.append(goods)
    # Write information
    user['knapsack'] = knapsack
    status = await writeUserInformation(userQQ, user)
    if status == error:
        return error
    return ok


async def singleAdventureExtract(bot, userQQ, userGroup):
    p = './HolyGrailWar/Config/Explore/SingleAdventure.json'
    content = await readFileToJSON(p)
    if content == error:
        raise GrailExcept
    replyMessage = ''
    replyMessage += await atQQ(userQQ)
    # Grain consumption
    status = await additionAndSubtractionOfUserInformationData(userQQ, 'resources', 'foodstuff', -100)
    if status == error:
        return error
    if str(status).find(insufficient) != -1:
        return replyMessage + '探险一次至少需要100粮食，你还剩下' + status.split(' ')[1] + '粮食，无法继续探险。'
    # Take the maximum number of events
    if 'eventlist' not in content:
        raise GrailExcept
    idList = []
    eventList = content['eventlist']
    for e in eventList:
        idList.append(e['id'])
    # Take random ID
    selectedID = int( random.choice(idList) )
    event = {}
    for e in eventList:
        if int( e['id'] ) == selectedID:
            event = e
    if event == {}:
        return error
    # event processing
    replyMessage += '【探险】' + await takeTheNameOfThePerson(bot, userQQ, userGroup)
    settlementInformation = []
    # Settlement of gold coins
    selectGold = 0
    if 'gold' in event:
        selectGold = event['gold']
        event['event'] = event['event'].replace(r'{gold}',str( event['gold'] ))
        settlementInformation.append('获得' + str(selectGold) + '金币')
    else:
        if ('goldmax' in event) and ('goldmin' in event):
            selectGold = random.randint(event['goldmin'], event['goldmax'])
            event['event'] = event['event'].replace(r'{gold}',str( selectGold ))
            if 'type' in event:
                if event['type'] == 'loss':
                    settlementInformation.append('失去' + str(selectGold) + '金币')
                    selectGold *= -1
            else:
                settlementInformation.append('获得' + str(selectGold) + '金币')
    # Operating user gold
    if selectGold != 0:
        status = await rigidGoldCoinAdditionAndSubtraction(userQQ, selectGold)
        if status == error:
            return error
    # Settlement items
    if 'goodsid' in event:
        goods = await getItemInformation(int( event['goodsid'] ))
        if goods == error:
            raise GrailExcept
        event['event'] = event['event'].replace(r'{goodsid}',('[' + str( goods['name'] ) + 'x' +
                                                str( event['amount'] ) + ']'))
        settlementInformation.append('获得' + ('[' + str( goods['name'] ) + 'x' +
                                                str( event['amount'] ) + ']'))
        # Operate user items
        status = await addItems(userQQ, goods['id'], event['amount'])
        if status == error:
            return error
    replyMessage += event['event'] + '\n\n' + '探险结算：\n' + str('，'.join(settlementInformation)) + '\n\n'
    replyMessage += await getUserRemainingResources(userQQ)
    return replyMessage


async def getMultipleExplorationEventTable(number):
    p = './HolyGrailWar/Config/Explore/MultipleExploration.json'
    if not os.path.exists(p):
        return error
    events = await readFileToJSON(p)
    eventList = events['eventlist']
    profit = {
        "addGold": 0,
        "lossGold": 0,
        "addFood": 0,
        "addItem": []
    }
    profit['event'] = set()
    if number <= 0:
        return error
    for n in range(number):
        isThereMistake = 0
        e = random.choice(eventList)
        # Goods handling
        if 'goodsid' in e:
            isThereMistake = 1
            if 'amount' not in e:
                return error
            # Failed item type exists
            if 'goodsid_fail' in e:
                # Success or failure
                for number in range(e['amount']):
                    rollPoint = random.randint(1,100)
                    if rollPoint > 60:
                        profit['addItem'].append(e['goodsid'])
                    else:
                        profit['addItem'].append(e['goodsid_fail'])
            else:
                for j in range(e['amount']):
                    profit['addItem'].append(e['goodsid'])
        # Settlement of gold coins
        if ('goldmax' in e) and ('goldmin' in e):
            isThereMistake = 1
            selectTheNumberOfGoldCoins = random.randint(e['goldmin'],e['goldmax'])
            if 'type' in e:
                profit['lossGold'] += int(selectTheNumberOfGoldCoins)
            else:
                profit['addGold'] += int(selectTheNumberOfGoldCoins)
        # Settling grain
        if ('foodmax' in e) and ('foodmin' in e):
            isThereMistake = 1
            selectGrainQuantity = random.randint(e['foodmin'],e['foodmax'])
            profit['addFood'] += int(selectGrainQuantity)
        if isThereMistake == 0:
            return error
        # Add event
        profit['event'].add(str(e['event']))
    profit['event'] = str('、'.join(profit['event']))
    return profit
    

async def grainOperation(userQQ):
    user = await userInformationQuery(userQQ)
    if user == error:
        raise GrailExcept
    resources = user['resources']
    foodstuff = resources['foodstuff']
    if foodstuff < 100:
        return insufficient + ' ' + str(foodstuff)
    number = int(int(foodstuff) / 100)
    # Grain reduction
    await additionAndSubtractionOfUserInformationData(userQQ, 'resources', 'foodstuff', -(100*number))
    return number
    

async def multipleExplorationExtraction(bot, userQQ, userGroup):
    # Judge whether it can be consumed
    status = await grainOperation(userQQ)
    if status == error:
        raise GrailExcept
    replyMessage = ''
    replyMessage += await atQQ(userQQ)
    if str(status).find(insufficient) != -1:
        return replyMessage + '探险一次至少需要100粮食，你还剩下' + status.split(' ')[1] + '粮食，无法继续探险。'
    # Continue event
    profit = await getMultipleExplorationEventTable(int(status))
    replyMessage += ('【探险】' + await takeTheNameOfThePerson(bot, userQQ, userGroup) + '进行了' +
                        str(status) + '次探险，经历了' + profit['event'] + 
                        '等大量的磨炼，脱胎换骨，收获颇丰。\n\n')
    replyMessage += '探险结算：\n'
    settlementContents = []
    isThereAnyOperationOnGoldCoin = 0
    # add Gold coin settlement
    if profit['addGold'] != 0 :
        isThereAnyOperationOnGoldCoin = 1
        settlementContents.append('获得' + str(profit['addGold']) + '金币')
    whetherThereIsGrainOperation = 0
    # foodstuff
    if profit['addFood'] != 0:
        whetherThereIsGrainOperation = 1
        settlementContents.append('获得' + str(profit['addFood']) + '粮食')
        status = await additionAndSubtractionOfUserInformationData(userQQ, 'resources', 'foodstuff', 
                                                                    int(profit['addFood']))
        if status == error:
            return error
    # loss Gold coin settlement  
    if profit['lossGold'] != 0:
        isThereAnyOperationOnGoldCoin = 1
        settlementContents.append('失去' + str(profit['lossGold']) + '金币')
    if isThereAnyOperationOnGoldCoin:
        status = await rigidGoldCoinAdditionAndSubtraction(userQQ, 
                                                int(profit['addGold'])-int(profit['lossGold']))
        if status == error:
            return error
    # Goods settlement
    if profit['addItem'] != []:
        listOfConvertedItems = {}
        for item in profit['addItem']:
            if str(item) in listOfConvertedItems:
                listOfConvertedItems[str(item)] += 1
            else:
                listOfConvertedItems[str(item)] = 1
        if listOfConvertedItems == {}:
            return error
        listOfSettlementItems = []
        for key,value in listOfConvertedItems.items():
            goods = await getItemInformation(int( key ))
            if goods == error:
                raise GrailExcept
            listOfSettlementItems.append('[' + str( goods['name'] ) + 'x' +
                                            str( value ) + ']')
            # Operate user items
            status = await addItems(userQQ, goods['id'], int(value))
            if status == error:
                return error
        settlementContents.append('获得' + ('，'.join(listOfSettlementItems)))
    # Add settlement message
    replyMessage += '，'.join(settlementContents) + '\n\n'
    # Determine if a virus is triggered
    getGoldCoinsActually = int(profit['addGold'])-int(profit['lossGold'])
    if getGoldCoinsActually < 0:
        getGoldCoinsActually = 0
    actualAccessToFood = profit['addFood']
    settlementParameters = [getGoldCoinsActually, actualAccessToFood]
    virusEvent = await Utils2plus.coronavirusEvent(userQQ, settlementParameters)
    if virusEvent[0] != '':
        replyMessage += virusEvent[0] + '\n\n本次探险实际收益：\n'
        # Actual income
        listOfActualBenefits = []
        if isThereAnyOperationOnGoldCoin:
            listOfActualBenefits.append('金币：' + 
                str( int( (profit['addGold']-profit['lossGold']) * (1 - virusEvent[1] / 100) ) ) + 
                '(-' + str(virusEvent[1]) + '%)')
        if whetherThereIsGrainOperation:
            listOfActualBenefits.append('粮食：' + 
                str( int( profit['addFood'] * (1 - virusEvent[1] / 100) ) ) + 
                '(-' + str(virusEvent[1]) + '%)')
        replyMessage += '，'.join(listOfActualBenefits) + '\n\n'
    # Surplus resources
    replyMessage += await getUserRemainingResources(userQQ)
    return replyMessage
        
        
    
        
            

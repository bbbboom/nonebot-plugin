# -*- coding: utf-8 -*-

import os
import aiofiles
import ujson
import random
from . import Utils
from .customException import GrailExcept

# Non fatal error type
error = 'error'
ok = 'ok'
insufficient = 'insufficient'

async def shop(userQQ):
    p = './HolyGrailWar/Config/UserAssistance/shop.json'
    pG = './HolyGrailWar/Config/Goods/Goods.json'
    content = await Utils.readFileToJSON(p)
    goodsContent = await Utils.readFileToJSON(pG)
    if content == error or goodsContent == error:
        raise GrailExcept
    msg = await Utils.atQQ(userQQ) + content['shop_prefix'] + '\n\n'
    goodsList = goodsContent['goodslist']
    for g in goodsList:
        if 'notsale' not in g:
            msg += g['name'] + ' 单价:' + str(g['price']) + '\n' + '  [!] ' + g['introduce'] + '\n'
    msg += content['shop_suffix']
    return str(msg)


async def knapsack(userQQ):
    p = './HolyGrailWar/Config/UserAssistance/shop.json'
    user = await Utils.userInformationQuery(userQQ)
    content = await Utils.readFileToJSON(p)
    if user == error or content == error:
        raise GrailExcept
    msg = (await Utils.atQQ(userQQ) + content['knapsack_prefix'] + '金币:' + 
                str(user['resources']['gold']) + '，粮食:' +
                   str(user['resources']['foodstuff']) + '\n')
    msg += content['backpack_split_line'] + '\n'
    userGoods = user['knapsack']
    if userGoods == []:
        msg += '背包空空如也哦\n'
    else:
        for g in userGoods:
            goodsInfo = await Utils.getItemInformation(g['id'])
            if goodsInfo == error:
                raise GrailExcept
            msg += goodsInfo['name'] + ' x ' + str(g['number']) + '\n' + '  [!] ' + goodsInfo['introduce'] + '\n'
    msg += content['backpack_split_line'] + '\n' + content['backpack_suffix']
    return str(msg)


async def shopHelp(userQQ):
    msg = await Utils.atQQ(userQQ)
    p = './HolyGrailWar/Config/UserAssistance/shop.json'
    content = await Utils.readFileToJSON(p)
    if content == error:
        raise GrailExcept
    msg += content['store_help_prefix']
    for command in content['store_help_main_content']:
        msg += '「' + command['name'] + '」:' + command['content'] + '\n'
    msg += '\n' + content['shop_help_tail']
    return msg


async def priceAfterGettingBonus(id):
    goodsInfo = await Utils.getItemInformation(id)
    if goodsInfo == error:
        raise GrailExcept
    price = goodsInfo['sale']
    p = './HolyGrailWar/Config/Goods/Goods.json'
    content = await Utils.readFileToJSON(p)
    if content == error:
        raise GrailExcept
    plus = content['sale_plus']
    tax = content['transaction_tax']
    selectiveAddition = random.uniform(float(plus['min']),float(plus['max']))
    price *= 1 + selectiveAddition
    return [price,tax]


async def deductionOfGoods(userQQ, id, number):
    user = await Utils.userInformationQuery(userQQ)
    if user == error:
        raise GrailExcept
    knapsack = user['knapsack']
    if knapsack == []:
        return error
    surplusQuantity = 0
    cleanKnapsack = []
    for k in knapsack:
        if k['id'] == id:
            if k['number'] > number:
                k['number'] -= number
                surplusQuantity = k['number']
                cleanKnapsack.append(k)
        else:
            cleanKnapsack.append(k)
    user['knapsack'] = cleanKnapsack
    await Utils.writeUserInformation(userQQ, user)
    return surplusQuantity


async def saleOfGoods(userQQ, id, number):
    user = await Utils.userInformationQuery(userQQ)
    msg = await Utils.atQQ(userQQ)
    if user == error:
        raise GrailExcept
    knapsack = user['knapsack']
    if knapsack == []:
        return msg + '您背包空空如也哦~'
    mark = 0
    for k in knapsack:
        if k['id'] == int(id):
            mark = 1
            goodsInfo = await Utils.getItemInformation(id)
            priceTax = await priceAfterGettingBonus(id)
            if k['number'] >= number:
                # Partial selling
                gold = int( priceTax[0] * number * (1 - priceTax[1]) )
                msg += ('【交易成功】卖出' + '[' + goodsInfo['name'] + 'x' + 
                        str(number) + ']，获得金币：' + str(gold) + '\n')
                # Deduction of goods
                status = await deductionOfGoods(userQQ, id, number)
            else:
                # Sell all
                gold = int( priceTax[0] * k['number'] * (1 - priceTax[1]) )
                msg += ('【交易成功】卖出全部' + '[' + goodsInfo['name'] + 'x' + 
                        str(k['number']) + ']，获得金币：' + str(gold) + '\n')
                # Deduction of goods
                status = await deductionOfGoods(userQQ, id, k['number'])
    if mark:
        if status == error:
            return error
    else:
        return error
    # Manipulation of gold coins
    await Utils.rigidGoldCoinAdditionAndSubtraction(userQQ, int(gold))
    # Tail information
    msg += ('* 商店老板在本单交易中收取 ' + str( priceTax[1] * 100 ) + '% ' + '交易税\n' + 
            '吼！欢迎下次光临！别忘了给五星好评哟！')
    return msg


async def getUserGoldCoins(userQQ):
    user = await Utils.userInformationQuery(userQQ)
    if user == error:
        raise GrailExcept
    userGold = user['resources']['gold']
    return int(userGold)


async def purchaseProps(userQQ, id, number):
    msg = await Utils.atQQ(userQQ)
    # Calculating purchase price
    goodsInfo = await Utils.getItemInformation(id)
    if 'price' not in goodsInfo:
        raise GrailExcept
    price = goodsInfo['price']
    gold = int(price * number)
    # Judge whether the gold coin is enough
    userGold = await getUserGoldCoins(userQQ)
    if userGold >= gold:
        # Operating items
        status = await Utils.addItems(userQQ, id, number)
        if status == error:
            return error
        # Manipulation of gold coins
        status = await Utils.rigidGoldCoinAdditionAndSubtraction(userQQ, (-1)*gold)
        msg += ('【交易成功】获得' + '[' + str(goodsInfo['name']) + 'x' + 
                    str(number) + ']，失去金币:' + str(gold) + '\n欢迎下次再来！')
    else:
        # Cannot afford
        theMaximumNumberToBuy = int( userGold / price )
        if theMaximumNumberToBuy == 0:
            msg += '金币不足，交易失败\n需要金币:' + str(gold) + '，拥有金币:' + str(userGold)
        else:
            # Full flower drop
            gold = theMaximumNumberToBuy * price
            # Operating items
            status = await Utils.addItems(userQQ, id, theMaximumNumberToBuy)
            if status == error:
                return error
            # Manipulation of gold coins
            status = await Utils.rigidGoldCoinAdditionAndSubtraction(userQQ, (-1)*gold)
            msg += ('【交易成功】获得' + '[' + str(goodsInfo['name']) + 'x' + 
                        str(theMaximumNumberToBuy) + ']，花光金币:' + str(gold) + '\n欢迎下次再来！')
    return msg


async def searchForItemPrice(userQQ, itemParameter):
    msg = await Utils.atQQ(userQQ)
    price = itemParameter[1]
    userGold = await getUserGoldCoins(userQQ)
    if userGold >= price:
        msg += str(itemParameter[0]) + '只卖 ' + str(price) + ' 哦'
    else:
        msg += str(itemParameter[0]) + '需要 ' + str(price) + ' 金币'
    return msg


async def backpackHelp(userQQ):
    msg = await Utils.atQQ(userQQ)
    p = './HolyGrailWar/Config/UserAssistance/BackpackHelpInformation.json'
    content = await Utils.readFileToJSON(p)
    if content == error:
        raise GrailExcept
    msg += content['prefix'] + '\n\n' + content['core'] + '\n\n' + content['suffix']
    return msg


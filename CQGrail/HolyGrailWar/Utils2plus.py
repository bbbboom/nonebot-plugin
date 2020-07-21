# -*- coding: utf-8 -*-

import os
import aiofiles
import ujson
import random
from . import Utils
from . import Utils2
from . import Utils3
from .customException import GrailExcept

# Non fatal error type
error = 'error'
ok = 'ok'

async def probabilityOfTriggeringAViralEvent():
    triggerProbability = random.randint(1,100)
    # Custom trigger probability
    customProbability = await Utils3.customParameterReading('coronavirus_event_trigger_probability')
    if triggerProbability > customProbability:
        return 0
    else:
        return 1


async def damageFromViruses():
    damage = random.randint(1,100)
    return damage


async def getBackpackAntiVirusItems(userQQ):
    backpack = await Utils3.getTheContentsOfUserIsBackpackUnit(userQQ)
    listOfAntiVirusItems = [7, 8, 9, 10]
    userSAntiVirusItemList = []
    for b in backpack:
        if b['id'] in listOfAntiVirusItems:
            userSAntiVirusItemList.append(b)
    return userSAntiVirusItemList


async def calculatingFinalDamage(userQQ, listOfAntiVirusItems, hurt):
    msg = ''
    if listOfAntiVirusItems == []:
        msg += '因没有任何防病毒道具，全额承受了 ' + str(hurt) + ' 点伤害。（可通过「商店」购买病毒防护道具）'
        return [msg, hurt]
    listOfAntiVirusItems.sort(key = lambda x:x['id'], reverse = True)
    for l in listOfAntiVirusItems:
        # antibody
        if l['id'] == 10:
            msg += '拥有 [冠状病毒抗体]，免疫 100 点病毒伤害，实际伤害为 0 点'
            # Deductions
            await Utils2.deductionOfGoods(userQQ, 10, 1)
            return [msg, 0]
        # Advanced gas mask
        if l['id'] == 9:
            # calculate Damage
            damage = hurt - 80
            if damage < 0:
                damage = 0
            msg += '拥有 [高级防毒面罩]，免疫 80 点病毒伤害，实际伤害为 ' + str(damage) + ' 点'
            # Deductions
            await Utils2.deductionOfGoods(userQQ, 9, 1)
            return [msg, damage]
        # N95
        if l['id'] == 8:
            # calculate Damage
            damage = hurt - 50
            if damage < 0:
                damage = 0
            msg += '拥有 [N95口罩]，免疫 50 点病毒伤害，实际伤害为 ' + str(damage) + ' 点'
            # Deductions
            await Utils2.deductionOfGoods(userQQ, 8, 1)
            return [msg, damage]
        # Ordinary mask
        if l['id'] == 7:
            # calculate Damage
            damage = hurt - 20
            if damage < 0:
                damage = 0
            msg += '拥有 [狗妈]，免疫 20 点病毒伤害，实际伤害为 ' + str(damage) + ' 点'
            # Deductions
            await Utils2.deductionOfGoods(userQQ, 7, 1)
            return [msg, damage]
    raise GrailExcept
        
            
async def coronavirusEvent(userQQ, settlementParameters):
    msg = ''
    # Calculate whether an event is triggered
    whetherToTriggerAnEvent = await probabilityOfTriggeringAViralEvent()
    if whetherToTriggerAnEvent == 1:
        # trigger event
        # Calculate Damage
        damage = await damageFromViruses()
        msg += ('◇ 触发探险特殊事件：\n💀' + '你感染了新型冠状病毒，受到' + str(damage) + 
                '点病毒伤害！探险收益降低。\n')
        # Calculate antiviral attenuation
        antiviralProps = await getBackpackAntiVirusItems(userQQ)
        damageList = await calculatingFinalDamage(userQQ, antiviralProps, damage)
        msg += damageList[0]
        # Deductions
        await Utils.rigidGoldCoinAdditionAndSubtraction(userQQ, 
                                        int((-1) * settlementParameters[0] * (damageList[1] / 100)))
        await Utils.additionAndSubtractionOfUserInformationData(userQQ, 'resources', 'foodstuff', 
                                        int((-1) * settlementParameters[1] * (damageList[1] / 100)))
        return [msg, damageList[1]]
    return [msg, 0]
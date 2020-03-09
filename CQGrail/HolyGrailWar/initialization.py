# -*- coding: utf-8 -*-

import os
import aiofiles
import ujson
from . import Utils
from dateutil.parser import parse
import datetime
from .customException import GrailExcept

# Non fatal error type
error = 'error'
ok = 'ok'

async def getOrWriteNumber(sequence, group, model = 'user'):
    userUID = 1
    groupUID = 1
    # user
    if sequence != 0:
        p = './HolyGrailWar/User/SequenceCode/UserUID.json'
        if not os.path.exists(p):
            firstUser = {
                "userlist": [
                        {
                    "qq": int(sequence),
                    "sequence": userUID
                    }
                ],
                "number": 1
            }
            async with aiofiles.open(p, 'w', encoding='utf-8') as f:
                await f.write(ujson.dumps(firstUser))
        else:
            users = await Utils.readFileToJSON(p)
            if users == error:
                raise GrailExcept
            userList = users['userlist']
            mark = False
            for u in userList:
                if u['qq'] == int(sequence):
                    mark = True
                    userUID = u['sequence']
                    break
            if mark == False:
                userUID = users['number'] + 1
                userINFO = {
                    "qq": int(sequence),
                    "sequence": userUID
                    }
                users['number'] += 1
                users['userlist'].append(userINFO)
                await Utils.writeTo(p, users)
    # group
    if group != 0:
        p = './HolyGrailWar/User/SequenceCode/GroupUID.json'
        if not os.path.exists(p):
            firstGroup = {
                "grouplist": [
                        {
                    "group": int(group),
                    "sequence": groupUID
                    }
                ],
                "number": 1
            }
            async with aiofiles.open(p, 'w', encoding='utf-8') as f:
                await f.write(ujson.dumps(firstGroup))
        else:
            groups = await Utils.readFileToJSON(p)
            if groups == error:
                raise GrailExcept
            groupList = groups['grouplist']
            mark = False
            for g in groupList:
                if g['group'] == int(group):
                    mark = True
                    groupUID = g['sequence']
                    break
            if mark == False:
                groupUID = groups['number'] + 1
                groupINFO = {
                    "group": int(group),
                    "sequence": groupUID
                    }
                groups['number'] += 1
                groups['grouplist'].append(groupINFO)
                await Utils.writeTo(p, groups)    
    if model == 'user':
        return 'U-' + str(userUID)
    else:
        return 'G-' + str(groupUID)


async def getCurrentDate():
    nowDate = str(datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d'))
    return nowDate


async def timeDifferenceFromNowOn(original):
    a = parse(str(original))
    b = parse(await getCurrentDate())
    return int((b-a).days)


async def determineWhetherToRegister(bot, userQQ, userGroup):
    p = './HolyGrailWar/User/Data/' + str(userQQ) + '.json'
    pTemplate = './HolyGrailWar/Config/Register/Template.json'
    if not os.path.exists(p):
        # register
        if not os.path.exists(pTemplate):
            raise GrailExcept
        registrationTemplate = await Utils.readFileToJSON(pTemplate)
        # Initialization parameters
        registrationTemplate['qq'] = int(userQQ)
        registrationTemplate['code_name'] = await getOrWriteNumber(userQQ, userGroup, 'user')
        registrationTemplate['register']['registration_group_number'] = int(userGroup)
        registrationTemplate['register']['registration_time'] = await getCurrentDate()
        registrationTemplate['register']['registered_nickname'] = await Utils.getUserNickname(bot, 
                                                                            userQQ, userGroup)
        registrationTemplate['register']['register_group_business_card'] = await Utils.takeTheNameOfThePerson(bot, 
                                                                            userQQ, userGroup)
        registrationTemplate['game']['last_game_time'] = await getCurrentDate()
        registrationTemplate['game']['last_game_time_group'] = int(userGroup)
        # Completion of registration
        await Utils.writeTo(p, registrationTemplate)
    else:
        await getOrWriteNumber(userQQ, userGroup, 'user')
        # Update play time
        user = await Utils.userInformationQuery(userQQ)
        user['game']['last_game_time'] = await getCurrentDate()
        user['game']['last_game_time_group'] = int(userGroup)
        user['game']['times_of_play'] += 1
        await Utils.writeUserInformation(userQQ, user)
    return ok



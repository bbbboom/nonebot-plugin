# -*- coding: utf-8 -*-

from . import Utils
from . import initialization

error = 'error'
ok = 'ok'

async def detectionInterval(userQQ):
    user = await Utils.userInformationQuery(userQQ)
    if user == error:
        return error
    lastTime = user['game']['last_game_time']
    intervalTime = await initialization.timeDifferenceFromNowOn(lastTime)
    if intervalTime >= 1:
        # Granting food
        user['resources']['foodstuff'] += 1000
        user['game']['last_game_time'] = await initialization.getCurrentDate()
        await Utils.writeUserInformation(userQQ, user)
    return ok
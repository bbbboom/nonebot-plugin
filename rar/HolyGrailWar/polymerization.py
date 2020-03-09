# -*- coding: utf-8 -*-

from . import matching
from . import dynamic

thesaurusReady = 0
botQQ = 0

error = 'error'

async def priorProcessing(msg):
    global botQQ
    atField = '[CQ:at,qq=' + str(botQQ) + ']'
    return msg.replace(atField, '').strip()

# Main starter
async def aggregationCall(bot, userQQ, userGroup, msg, rawMsg):
    global thesaurusReady
    global botQQ
    if thesaurusReady == 0:
        await matching.thesaurusInitialization()
        botQQ = await bot.get_login_info()
        botQQ = int(botQQ['user_id'])
        thesaurusReady = 1
    # Clean up at messages
    cleanMsg = await priorProcessing(msg)
    # Determine whether to register
    status = await matching.whetherTheUserCanUseTheCommand(userQQ)
    if status != error:
        # Registered
        # Trigger distribution function
        await dynamic.detectionInterval(userQQ)
        # Knapsack function
        await matching.knapsackFunction(bot, userQQ, userGroup, cleanMsg)
        # Store function
        await matching.storeKeywordJump(bot, userQQ, userGroup, cleanMsg)
        # Follower list function
        await matching.followerList(bot, userQQ, userGroup, cleanMsg)
        # Follower details function
        await matching.enquiryDetails(bot, userQQ, userGroup, cleanMsg)
        # Free and obedient function
        await matching.releaseFollower(bot, userQQ, userGroup, cleanMsg)
        # Attack function
        await matching.attackFunctionIdentification(bot, userQQ, userGroup, msg, rawMsg)
        # Leaderboard function
        await matching.leaderboardRecognition(bot, userQQ, userGroup, msg)
    # Adventure function
    await matching.adventureFunction(bot, userQQ, userGroup, cleanMsg)
    # Follower function
    await matching.identifyWhetherItIsACaptureCommand(bot, userQQ, userGroup, msg, rawMsg)
    # Main help
    await matching.userSMainHelpManual(bot, userQQ, userGroup, cleanMsg)

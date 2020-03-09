# -*- coding: utf-8 -*-

from . import initialization
from . import Utils
from . import Utils2
from . import Utils3
from . import Utils4
from . import Utils3plus

error = 'error'
ok = 'ok'

async def singleExpeditionDistribution(bot, userQQ, userGroup):
    # Refresh registration
    await initialization.determineWhetherToRegister(bot, userQQ, userGroup)
    # Get game information
    msg = await Utils.singleAdventureExtract(bot, userQQ, userGroup)
    if msg == error:
        return error
    # Send out
    await bot.send_group_msg(group_id = int(userGroup), message = str(msg))


async def multipleExpeditionsDistribution(bot, userQQ, userGroup):
    # Refresh registration
    await initialization.determineWhetherToRegister(bot, userQQ, userGroup)
    # Get game information
    msg = await Utils.multipleExplorationExtraction(bot, userQQ, userGroup)
    if msg == error:
        return error
    # Send out
    await bot.send_group_msg(group_id = int(userGroup), message = str(msg))


async def storePageDistribution(bot, userQQ, userGroup):
    # pick up information
    msg = await Utils2.shop(userQQ)
    if msg == error:
        return error
    # Send out
    await bot.send_group_msg(group_id = int(userGroup), message = str(msg))


async def purchaseItems(bot, userQQ, userGroup, purchaseParameters):
    # pick up information
    msg = await Utils2.purchaseProps(userQQ, purchaseParameters[0], purchaseParameters[1])
    if msg == error:
        return error
    # Send out
    await bot.send_group_msg(group_id = int(userGroup), message = str(msg))


async def sellGoods(bot, userQQ, userGroup, purchaseParameters):
    # pick up information
    msg = await Utils2.saleOfGoods(userQQ, purchaseParameters[0], purchaseParameters[1])
    if msg == error:
        return error
    # Send out
    await bot.send_group_msg(group_id = int(userGroup), message = str(msg))


async def inquiryPrice(bot, userQQ, userGroup, queryParameters):
    # pick up information
    msg = await Utils2.searchForItemPrice(userQQ, queryParameters)
    if msg == error:
        return error
    # Send out
    await bot.send_group_msg(group_id = int(userGroup), message = str(msg))


async def storeHelpDistribution(bot, userQQ, userGroup):
    # pick up information
    msg = await Utils2.shopHelp(userQQ)
    if msg == error:
        return error
    # Send out
    await bot.send_group_msg(group_id = int(userGroup), message = str(msg))


async def backpackFunctionDistribution(bot, userQQ, userGroup):
    # pick up information
    msg = await Utils2.knapsack(userQQ)
    if msg == error:
        return error
    # Send out
    await bot.send_group_msg(group_id = int(userGroup), message = str(msg))


async def backpackHelpDistribution(bot, userQQ, userGroup):
    # pick up information
    msg = await Utils2.backpackHelp(userQQ)
    if msg == error:
        return error
    # Send out
    await bot.send_group_msg(group_id = int(userGroup), message = str(msg))


async def captureFunctionDistribution(bot, userQQ, followQQ, userGroup):
    # Refresh registration
    await initialization.determineWhetherToRegister(bot, userQQ, userGroup)
    # pick up information
    msgList = await Utils3.captureTheFirstLevelOfTreatment(bot, userQQ, followQQ, userGroup)
    if isinstance(msgList, list):
        # In snap range
        if msgList[0] == 0:
            # fail
            await bot.send_group_msg(group_id = int(userGroup), message = str(msgList[1]))
        else:
            # Succeed
            await bot.send_group_msg(group_id = int(userGroup), message = str(msgList[1]))
            await bot.send_group_msg(group_id = int(userGroup), message = str(msgList[3]))
    else:
        # Out of range
        await bot.send_group_msg(group_id = int(userGroup), message = str(msgList))


async def masterHelpDistribution(bot, userQQ, userGroup):
    # pick up information
    msg = await Utils3.helpMenu(userQQ)
    if msg == error:
        return error
    # Send out
    await bot.send_group_msg(group_id = int(userGroup), message = str(msg))


async def followerListDistributor(bot, userQQ, userGroup):
    # pick up information
    msg = await Utils3plus.followerList(userQQ)
    if msg == error:
        return error
    # Send out
    await bot.send_group_msg(group_id = int(userGroup), message = str(msg))


async def followerDetailsDistributor(bot, userQQ, userGroup, followQQ):
    # pick up information
    msg = await Utils3plus.detailsOfTheAttendant(userQQ, followQQ)
    if msg == error:
        return error
    # Send out
    await bot.send_group_msg(group_id = int(userGroup), message = str(msg))


async def oneClickAttackDistributor(bot, userQQ, userGroup, targetQQ):
    # pick up information
    msg = await Utils3plus.determineIfAOneClickAttackIsPossible(userQQ, targetQQ,  model = 'one_click_attack')
    if msg == error:
        return error
    # Send out
    await bot.send_group_msg(group_id = int(userGroup), message = str(msg))


async def singleStepAttackDistribution(bot, userQQ, userGroup, targetQQ):
    # pick up information
    msg = await Utils3plus.isItPossibleToPerformASingleAttack(userQQ, targetQQ)
    if msg == error:
        return error
    # Send out
    await bot.send_group_msg(group_id = int(userGroup), message = str(msg))


async def singleStepDistributor2(bot, userGroup, status, id):
    # pick up information
    msg = await Utils3plus.singleStepAttack(status, id)
    if msg == error:
        return error
    # Send out
    await bot.send_group_msg(group_id = int(userGroup), message = str(msg))


async def releaseFollowerDistributor(bot, userQQ, userGroup, followQQ):
    # pick up information
    msg = await Utils3plus.releaseAttendants(userQQ, followQQ)
    if msg == error:
        return error
    # Send out
    await bot.send_group_msg(group_id = int(userGroup), message = str(msg))


async def distributeFollowerRankings(bot, userQQ, userGroup):
    # pick up information
    msg = await Utils4.summaryFunction(bot, userQQ, userGroup, model = 'share_leaderboard')
    if msg == error:
        return error
    # Send out
    await bot.send_group_msg(group_id = int(userGroup), message = str(msg))


async def goldCoinLeaderboardDistribution(bot, userQQ, userGroup):
    # pick up information
    msg = await Utils4.summaryFunction(bot, userQQ, userGroup, model = 'gold_coin_ranking')
    if msg == error:
        return error
    # Send out
    await bot.send_group_msg(group_id = int(userGroup), message = str(msg))


async def fightingLeaderboardDistribution(bot, userQQ, userGroup):
    # pick up information
    msg = await Utils4.summaryFunction(bot, userQQ, userGroup, model = 'fighting_leaderboard')
    if msg == error:
        return error
    # Send out
    await bot.send_group_msg(group_id = int(userGroup), message = str(msg))


async def distributeWithQualityLeaderboards(bot, userQQ, userGroup):
    # pick up information
    msg = await Utils4.summaryFunction(bot, userQQ, userGroup, model = 'follower_qualifications_list')
    if msg == error:
        return error
    # Send out
    await bot.send_group_msg(group_id = int(userGroup), message = str(msg))
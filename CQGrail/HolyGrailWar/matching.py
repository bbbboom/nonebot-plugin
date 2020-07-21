# -*- coding: utf-8 -*-

from . import distributionMessage
from . import Utils
from . import Utils3
from . import Utils3plus
import jieba_fast as jieba
import re
from .customException import GrailExcept

# Non fatal error type
error = 'error'
ok = 'ok'

async def thesaurusInitialization():
    # Dynamically load Thesaurus
    _p = './HolyGrailWar/Config/Goods/Goods.json'
    _content = await Utils.readFileToJSON(_p)
    for _g in _content['goodslist']:
        jieba.add_word(_g['name'])
        for _a in _g['abbreviation']:
            jieba.add_word(_a)

async def exactMatchCommand(commandList, msg):
    mark = 0
    for c in commandList:
        if msg == str(c):
            mark = 1
            break
    return mark


async def fuzzyMatchCommand(commandList, msg):
    mark = 0
    for c in commandList:
        if msg.find(str(c)) != -1:
            mark = 1
            break
    return mark


async def judgeWhetherItHasBeenRegistered(userQQ):
    status = await Utils.userInformationQuery(userQQ)
    if status == error:
        return error
    return ok


async def getTheNumberOfPossiblePurchases(wordSegmentationTable):
    for w in wordSegmentationTable:
        if w.isdecimal():
            if int(w) > 0:
                return int(w)
            else:
                return 1
    return 1


async def quickSearchOfItemKeywords(msg, _model = 'sell_out'):
    p = './HolyGrailWar/Config/Goods/Goods.json'
    content = await Utils.readFileToJSON(p)
    if content == error:
        raise GrailExcept
    goodsList = content['goodslist']
    segmentationResult = jieba.lcut(msg)
    designatedPopUp = 0
    if _model == 'purchase' or _model == 'sell_out':
        # Find figures
        numberMatchResults = await getTheNumberOfPossiblePurchases(segmentationResult)
        for i in segmentationResult:
            for g in goodsList:
                # May pop up
                if 'eject' in g:
                    for i_ in segmentationResult:
                        if i_ in g['eject']:
                            designatedPopUp = 1
                            break
                if designatedPopUp == 1:
                    designatedPopUp = 0
                    continue
                if _model == 'purchase':
                    if 'notsale' in g:
                        if g['notsale'] == True:
                            break
                if g['name'] == str(i):
                    return [g['id'],int(numberMatchResults)]
                for a in g['abbreviation']:
                    if a == str(i):
                        return [g['id'],int(numberMatchResults)]
    elif _model == 'check_the_price':
        # Price checking mode
        for i in segmentationResult:
            for g in goodsList:
                # May pop up
                if 'eject' in g:
                    for i_ in segmentationResult:
                        if i_ in g['eject']:
                            designatedPopUp = 1
                            break
                if designatedPopUp == 1:
                    designatedPopUp = 0
                    continue
                if 'notsale' in g:
                    if g['notsale'] == True:
                        break
                if g['name'] == str(i):
                    return [g['name'],g['price']]
                for a in g['abbreviation']:
                    if a == str(i):
                        return [g['name'],g['price']]
    return error


async def storeLevel2Identification(msg, model = 'sell_out'):
    status = await quickSearchOfItemKeywords(msg, _model = model)
    if status == error:
        return error
    return status


async def storeFirstLevelIdentification(bot, userQQ, userGroup, msg):
    purchaseOrderList = ['购买','购入','买进']
    if await fuzzyMatchCommand(purchaseOrderList, msg) == 1:
        status = await storeLevel2Identification(msg, model = 'purchase')
        if status != error:
            # Pull up purchase function
            await distributionMessage.purchaseItems(bot, userQQ, userGroup, status)
    sellOrderList = ['卖出','售出','出售','卖掉']
    if await fuzzyMatchCommand(sellOrderList, msg) == 1:
        status = await storeLevel2Identification(msg, model = 'sell_out')
        if status != error:
            # Pull up sell function
            await distributionMessage.sellGoods(bot, userQQ, userGroup, status)
    queryPriceCommandList = ['多少钱','怎么卖','多钱','价格多少']
    if await fuzzyMatchCommand(queryPriceCommandList, msg) == 1:
        status = await storeLevel2Identification(msg, model = 'check_the_price')
        if status != error:
            # Pull up price function
            await distributionMessage.inquiryPrice(bot, userQQ, userGroup, status)


async def storeKeywordJump(bot, userQQ, userGroup, msg):
    # Judge whether it has been registered
    if await judgeWhetherItHasBeenRegistered(userQQ) == error:
        return error
    # perfect match
    if msg == '商店':
        # Direct distribution
        await distributionMessage.storePageDistribution(bot, userQQ, userGroup)
    elif msg == '商店帮助':
        await distributionMessage.storeHelpDistribution(bot, userQQ, userGroup)
    else:
        # Store function identification
        await storeFirstLevelIdentification(bot, userQQ, userGroup, msg)


async def knapsackFunction(bot, userQQ, userGroup, msg):
    # Judge whether it has been registered
    if await judgeWhetherItHasBeenRegistered(userQQ) == error:
        return error
    # perfect match
    backpackCommandList = ['背包','道具']
    backpackHelpCommandList = ['物品帮助','背包帮助','道具帮助']
    if await exactMatchCommand(backpackCommandList, msg) == 1:
        # Pull up the distribution
        await distributionMessage.backpackFunctionDistribution(bot, userQQ, userGroup)
    elif await exactMatchCommand(backpackHelpCommandList, msg) == 1:
        # Pull up the distribution
        await distributionMessage.storeHelpDistribution(bot, userQQ, userGroup)


async def adventureFunction(bot, userQQ, userGroup, msg):
    # Single Adventure
    singleExpeditionCommandList = ['探险']
    if await exactMatchCommand(singleExpeditionCommandList, msg) == 1:
        # distribute
        await distributionMessage.singleExpeditionDistribution(bot, userQQ, userGroup)
    # Multiple explorations
    multipleExplorationCommandList = ['一键探险','一件探险','一间探险','意见探险']
    if await exactMatchCommand(multipleExplorationCommandList, msg) == 1:
        # distribute
        await distributionMessage.multipleExpeditionsDistribution(bot, userQQ, userGroup)


async def extractAtPeople(botQQ, msg):
    findQQList = re.findall('\[CQ:at,qq=([1-9][0-9]{4,})\]',msg)
    if len(findQQList) == 1:
        return int(findQQList[0])
    if len(findQQList) == 2:
        if int(botQQ) == int(findQQList[0]) and int(botQQ) == int(findQQList[1]):
            return int(botQQ)
        elif int(botQQ) == int(findQQList[0]) and int(botQQ) != int(findQQList[1]):
            return int(findQQList[1])
        elif int(botQQ) != int(findQQList[0]) and int(botQQ) == int(findQQList[1]):
            return int(findQQList[0])
    return error


async def preventingFalseAt(rawMsg):
    for m in rawMsg:
        if m['type'] == 'at':
            return 1
    return 0


async def identifyWhetherItIsACaptureCommand(bot, userQQ, userGroup, msg, rawMsg):
    if msg.find('捕捉') != -1:
        # Exclude non group cases
        if await preventingFalseAt(rawMsg) == 0:
            return error
        # Extract at people
        botQQ = await bot.get_login_info()
        followQQ = await extractAtPeople(botQQ['user_id'], msg)
        if followQQ == error or followQQ == userQQ:
            return error
        # Pull up distribution function
        await distributionMessage.captureFunctionDistribution(bot, userQQ, followQQ, userGroup)
        return ok
    return error


async def userSMainHelpManual(bot, userQQ, userGroup, msg):
    helpCommandList = ['帮助','help','/help']
    if await exactMatchCommand(helpCommandList, msg) == 1:
        # distribute
        await distributionMessage.masterHelpDistribution(bot, userQQ, userGroup)
        

async def followerList(bot, userQQ, userGroup, msg):
    CommandList = ['随从列表']
    if await exactMatchCommand(CommandList, msg) == 1:
        # distribute
        await distributionMessage.followerListDistributor(bot, userQQ, userGroup)


async def whetherTheUserCanUseTheCommand(userQQ):
    user = await Utils.userInformationQuery(userQQ)
    if user == error:
        return error
    return ok


async def enquiryDetails(bot, userQQ, userGroup, msg):
    # Judge whether there are followers
    follow = await Utils3.getInformationOfUserSFollowerModule(userQQ)
    if follow['number'] == 0:
        return error
    # Check whether it conforms to the format
    if msg.find('随从详情') != -1:
        # Remove fixed fields
        msg = msg.replace('随从详情','').strip()
        # Participle of original news
        listOfOriginalWordSegmentation = [msg]
        listOfOriginalWordSegmentation += jieba.lcut(msg)
        # Add follower name to Library
        for l in listOfOriginalWordSegmentation:
            for f in follow['follower_information']:
                # perfect match
                if f['name'] == l:
                    await distributionMessage.followerDetailsDistributor(bot, userQQ, 
                                                                        userGroup, f['qq'])
                    return ok
                # Word segmentation
                listOfFollowerNames = jieba.lcut(f['name'])
                for l_ in listOfFollowerNames:
                    if l_ == l:
                        await distributionMessage.followerDetailsDistributor(bot, userQQ, 
                                                                        userGroup, f['qq'])
                        return ok


async def attackFunctionIdentification(bot, userQQ, userGroup, msg, rawMsg):
    if msg[0].isdecimal():
        number = int(msg[0])
        if number < 10 and number > 0:
            # Check whether the identification exists
            status = await Utils3plus.theSecondStepOfSingleCombat(userQQ)
            if status != 0:
                # Identification of existence
                await distributionMessage.singleStepDistributor2(bot, userGroup, status, number)
                return ok
    if msg.find('攻击') != -1:
        # Exclude non group cases
        if await preventingFalseAt(rawMsg) == 0:
            return error
        # Extract at people
        botQQ = await bot.get_login_info()
        targetQQ = await extractAtPeople(botQQ['user_id'], msg)
        if targetQQ == error:
            return error
        # Judge whether it is a one click attack or an attack
        if msg.find('一键攻击') != -1:
            # Pull up distribution function
            await distributionMessage.oneClickAttackDistributor(bot, userQQ, userGroup, targetQQ)
        else:
            # Pull up distribution function
            await distributionMessage.singleStepAttackDistribution(bot, userQQ, userGroup, targetQQ)
        return ok
    return error


async def releaseFollower(bot, userQQ, userGroup, msg):
    # Judge whether there are followers
    follow = await Utils3.getInformationOfUserSFollowerModule(userQQ)
    if follow['number'] == 0:
        return error
    # Check whether it conforms to the format
    if msg.find('放生') != -1:
        # Remove fixed fields
        msg = msg.replace('放生','').strip()
        # Participle of original news
        listOfOriginalWordSegmentation = [msg]
        listOfOriginalWordSegmentation += jieba.lcut(msg)
        # Add follower name to Library
        for l in listOfOriginalWordSegmentation:
            for f in follow['follower_information']:
                # perfect match
                if f['name'] == l:
                    await distributionMessage.releaseFollowerDistributor(bot, userQQ, 
                                                                        userGroup, f['qq'])
                    return ok
                # Word segmentation
                listOfFollowerNames = jieba.lcut(f['name'])
                for l_ in listOfFollowerNames:
                    if l_ == l:
                        await distributionMessage.releaseFollowerDistributor(bot, userQQ, 
                                                                        userGroup, f['qq'])
                        return ok
    

async def leaderboardRecognition(bot, userQQ, userGroup, msg):
    followerOrderList = ['随从热度排行', '随从热度']
    if await exactMatchCommand(followerOrderList, msg) == 1:
        # distribute
        await distributionMessage.distributeFollowerRankings(bot, userQQ, userGroup)
    goldCoinLeaderboardOrder = ['金币排行']
    if await exactMatchCommand(goldCoinLeaderboardOrder, msg) == 1:
        # distribute
        await distributionMessage.goldCoinLeaderboardDistribution(bot, userQQ, userGroup)
    followerOrderList = ['战斗力排行']
    if await exactMatchCommand(followerOrderList, msg) == 1:
        # distribute
        await distributionMessage.fightingLeaderboardDistribution(bot, userQQ, userGroup)
    followerOrderList = ['随从资质排行']
    if await exactMatchCommand(followerOrderList, msg) == 1:
        # distribute
        await distributionMessage.distributeWithQualityLeaderboards(bot, userQQ, userGroup)

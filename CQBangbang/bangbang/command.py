# -*- coding:utf-8 -*- 

async def reasonable(msg,keyList,model = 'id'):
    msg = str(msg)
    response = [0,0]
    for key in keyList:
        if model == 'id':
            try:
                command = msg.split(' ')[0]
                number = msg.split(' ')[1]
                # ' ' 模式
                if command == key and int(number) > 900 and int(number) < 30000:
                    response[0] = 1
                    response[1] = int(number)
            except:
                try:
                    # '.' 模式
                    if msg.find('.' + str(key)) != -1:
                        number = int(msg[1 + len(key):])
                        if int(number) > 900 and int(number) < 30000:
                            response[0] = 1
                            response[1] = int(number)
                except:
                    pass
        # model = 'searchName' 模式
        elif model == 'searchName':
            try:
                command = msg.split(' ')[0]
                nameList = msg[msg.find(' ') + 1:].split(' ')
                screenNameList = [[],[]]
                for name in nameList:
                    if name.find('#') != -1:
                        screenNameList[1].append(name[1:])
                    else:
                        screenNameList[0].append(name)
                # ' ' 模式
                if command == key:
                    response[0] = 1
                    response[1] = screenNameList
            except:
                pass
    return response
        

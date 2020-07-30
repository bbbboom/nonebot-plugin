from PIL import Image, ImageDraw
from nonebot import *
from io import BytesIO
import os
import random
import requests
import aiocqhttp

_avatar_size = 139
_center_pos = (17, 180)

_toppest = 164
_downest = 504

@on_command('throw', aliases=('丢',), only_to_me=False)
async def throw(session: CommandSession):
    throwed_whos = session.state.get('whos')
    avatar_img = 'http://q.qlogo.cn/headimg_dl?dst_uin={QQ}&spec=640'
    if not throwed_whos:
        throwed_who = session.event['user_id']
    else:
        throwed_who = throwed_whos[0]
    avatar_img = avatar_img.format(QQ=throwed_who)
    res = requests.get(avatar_img)
    avatar = Image.open(BytesIO(res.content)).convert('RGBA')
    avatar = get_circle_avatar(avatar, _avatar_size)

    rotate_angel = random.randrange(0, 360)
    throw_img = Image.open('image/throw.png').convert('RGBA')
    throw_img.paste(avatar.rotate(rotate_angel), _center_pos, avatar.rotate(rotate_angel))
    throw_img.save(f'image/avatar/{throwed_who}.png')

    send_message = MessageSegment.image(f'{os.getcwd()}/image/avatar/{throwed_who}.png')
    try:
        await get_bot().delete_msg(message_id=session.event['message_id'], self_id=session.event['self_id'])
    except aiocqhttp.exceptions.ActionFailed as e:
        pass
    await session.send(send_message)

@throw.args_parser
async def _(session: CommandSession):
    message = session.event['message']
    throwed_whos = []
    for segment in message:
        if segment['type'] == 'at':
            throwed_whos.append(segment['data']['qq'])
    if not len(throwed_whos) == 0:
        session.state['whos'] = throwed_whos

@on_natural_language(keywords={'丢', 'throw', }, only_to_me=False)
async def _(session: NLPSession):
    message = session.event['message']
    intent = 100.0
    throwed_whos = []
    s_msg = session.msg_text.replace('丢人', '').replace('丢', '').replace('throw', '')
    if len(s_msg.strip()) >= 1:
        print(s_msg)
        return
    for segment in message:
        if segment['type'] == 'at':
            throwed_whos.append(segment['data']['qq'])

    if not len(throwed_whos) == 0:
        return IntentCommand(intent, 'throw', current_arg=throwed_whos)


@on_command('creep', aliases=('爬','爪巴'),  only_to_me=False)
async def creep(session: CommandSession):
    creeped_whos = session.state.get('whos')
    id = session.state.get('id')
    pa_num = len(os.listdir('image/pa/'))-1
    if not id or id > pa_num:
        id = random.randrange(0, pa_num)
    avatar_img = 'http://q.qlogo.cn/headimg_dl?dst_uin={QQ}&spec=640'
    if not creeped_whos:
        session.finish('')
    else:
        creeped_who = creeped_whos[0]
    if int(creeped_who) == session.self_id:
        print(creeped_who)
        egg = MessageSegment.image(f'{os.getcwd()}/image/不爬.jpg')
        await session.finish(egg, at_sender=True)
    avatar_img = avatar_img.format(QQ=creeped_who)
    res = requests.get(avatar_img)
    avatar = Image.open(BytesIO(res.content)).convert('RGBA')
    avatar = get_circle_avatar(avatar, 100)

    creep_img = Image.open(f'image/pa/爬{id}.jpg').convert('RGBA')
    creep_img = creep_img.resize((500, 500), Image.ANTIALIAS)
    creep_img.paste(avatar, (0, 400, 100, 500), avatar)
    creep_img.save(f'image/avatar/{creeped_who}_creeped.png')

    send_message = MessageSegment.image(f'{os.getcwd()}/image/avatar/{creeped_who}_creeped.png')
    try:
        await get_bot().delete_msg(message_id=session.event['message_id'], self_id=session.event['self_id'])
    except aiocqhttp.exceptions.ActionFailed as e:
        pass
    await session.send(send_message)

@creep.args_parser
async def _(session: CommandSession):
    message = session.event['message']
    creeped_whos = []
    for segment in message:
        if segment['type'] == 'at':
            creeped_whos.append(segment['data']['qq'])
        if segment['type'] == 'text':
            s_msg = segment['data']['text']
            if s_msg.isdigit() and (int(s_msg) < 55 and int(s_msg) > 0):
                session.state['id'] = int(s_msg)

    if not len(creeped_whos) == 0:
        session.state['whos'] = creeped_whos

@on_natural_language(keywords={'爬', '爪巴', }, only_to_me=False)
async def _(session: NLPSession):
    message = session.event['message']
    intent = 100.0
    creeped_whos = []
    s_msg = session.msg_text.replace('爬', '').replace('爪巴', '')
    if len(s_msg.strip()) > 1:
        print(s_msg)
        return
    for segment in message:
        if segment['type'] == 'at':
            creeped_whos.append(segment['data']['qq'])

    if not len(creeped_whos) == 0:
        return IntentCommand(intent, 'creep', current_arg=creeped_whos)


def get_circle_avatar(avatar: Image, size: int):
    avatar.thumbnail((size, size))

    scale = 5
    mask = Image.new('L', (size*scale, size*scale), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size * scale, size * scale), fill=255)
    mask = mask.resize((size, size), Image.ANTIALIAS)

    ret_img = avatar.copy()
    ret_img.putalpha(mask)

    return ret_img
import io
import random
import re
import json

import nonebot
import numpy
import requests
from matplotlib import pyplot as plt
from nonebot.permission import SUPERUSER
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Message, Event, Bot, GroupMessageEvent, PrivateMessageEvent, GROUP_ADMIN, \
    GROUP_OWNER
from nonebot import on_command
from src.libraries.image import *
from src.libraries.searchManage import SearchManager
from src.libraries.sendAction import *
from src.libraries.tool import hash
from src.libraries.permissionManage import PermissionManager

oriurl = "http://ocgcard.fireinsect.top/"
# oriurl = "http://localhost:3399/"
obj = []
pm = PermissionManager()
sm = SearchManager()


# ==========工具变量、方法=============================


def verifySid(sid: str):
    try:
        sType, sId = sid.split('_')
        if sType in ['group', 'user']:
            if sId.isdigit():
                return True
        return False
    except:
        return False


# ===============功能==================================================

ocghelp = on_command('ygo help', aliases={'ygo 帮助', 'ygohelp', 'ygo帮助'})


@ocghelp.handle()
async def _(bot: Bot, event: Event, state: T_State):
    txt = '''欧尼酱~你可以对查卡姬说如下命令哟~
    随机一卡(抽一张卡)
    今日卡运   查看今天打牌运势~
    查卡 ygo卡名 (怪兽|魔法|陷阱) (页码)   查询对应卡牌~
    价格查询 卡名 (页码)    查询集换社价格
    查询饼图    查询ygo饼图
    抽卡功能 on | off   开/关抽卡功能(仅限管理)
    查卡方式 1|2|3  切换查卡方式'''
    await ocghelp.send(Message([{
        "type": "image",
        "data": {
            "file": f"base64://{str(image_to_base64(text_to_image(txt)), encoding='utf-8')}"
        }
    }]))


# ensearch_card = on_command("en查卡", aliases={'英文查卡'})
#
#
# @ensearch_card.handle()
# async def _(bot: Bot, event: Event, state: T_State):
#     text = event.get_message()
#     regex = "(.+) (page)?([0-9]+)?"
#     search_group = re.match(regex, str(text))
#     try:
#         print(search_group.groups()[2])
#     except Exception as e:
#         text = text + " 1"
#         search_group = re.match(regex, str(text))
#     try:
#         if search_group.groups()[2] is None:
#             text = text + " 1"
#             search_group = re.match(regex, str(text))
#         name = search_group.groups()[0]
#         page = search_group.groups()[2]
#         url = oriurl + "getCardByEn?enName=" + name + "&page=" + page
#         result = requests.get(url).text
#         js = json.loads(result)
#     except Exception as e:
#         await ensearch_card.send("咿呀？查询失败了呢")
#     if isinstance(event, PrivateMessageEvent):
#         await send(js)
#     elif isinstance(event, GroupMessageEvent):
#         await send2(js, bot, event)


search_card = on_command("查卡")


@search_card.handle()
async def _0(bot: Bot, event: Event, state: T_State):
    if isinstance(event, PrivateMessageEvent):
        sessionId = 'user_' + str(event.user_id)
        userType = 'private'
    if isinstance(event, GroupMessageEvent):
        sessionId = 'group_' + str(event.group_id)
        userType = 'group'
    regex = "(.+) (page)?([0-9]+)?"

    text = str(event.get_message()).strip()
    search_group = re.match(regex, text)
    try:
        print(search_group.groups()[2])
    except Exception as e:
        text = text + " 1"
        search_group = re.match(regex, str(text))

    try:
        if search_group.groups()[2] is None:
            text = text + " 1"
            search_group = re.match(regex, str(text))
        page = search_group.groups()[2]
        textNext = search_group.groups()[0]
        search_group2 = re.search(r" (?:魔法|怪兽|陷阱)\Z", textNext)
        if search_group2 is None:
            name = textNext
            url = oriurl + "getCard?name={0}&page={1}".format(name, page)
        else:
            type = search_group2.group(0).strip()
            name = re.sub(r" (?:魔法|怪兽|陷阱)\Z", "", textNext).strip()
            url = oriurl + "getCard?name={0}&type={1}&page={2}".format(name, type, page)
        print("----------")
        print(name)
        print(url)
        result = requests.get(url).text
        js = json.loads(result)
    except Exception as e:
        await search_card.finish("咿呀？查询失败了呢")
    state['js'] = js
    if js['data']['amount'] == 0:
        sendNosearch(search_card)
    elif isinstance(event, PrivateMessageEvent):
        await send2(js, search_card)
    elif isinstance(event, GroupMessageEvent):
        typee = sm.CheckType(sessionId)
        state['type'] = typee
        if typee == 1:
            await send2(js, search_card)
        elif typee == 2:
            await send(js, bot, event, search_card)
        else:
            await send3(js, search_card)


@search_card.got("num")
async def _(bot: Bot, event: Event, state: T_State):
    num = str(state['num'])
    if num.isdigit():
        if isinstance(event, PrivateMessageEvent):
            typee = 1
        elif isinstance(event, GroupMessageEvent):
            typee = int(state['type'])
        js = state['js']
        len = int(js['data']['amount'])
        chose = int(num)
        if 1 <= chose <= len:
            if typee == 1:
                await send2(js, search_card, chose)
            elif typee == 2:
                await send(js, bot, event, search_card, chose)
            else:
                await send3(js, search_card, chose)


# id_card = on_command("查id")
#
#
# @id_card.handle()
# async def _(bot: Bot, event: Event, state: T_State):
#     regex = "([0-9]+)"
#     text = str(event.get_message()).strip()
#     search_group = re.match(regex, text)
#     try:
#         id = search_group.groups()[0]
#         url = oriurl + "searchCardId?cardId=" + id
#         result = requests.get(url).text
#         js = json.loads(result)
#     except Exception as e:
#         await search_card.send("咿呀？查询失败了呢")
#     if isinstance(event, PrivateMessageEvent):
#         await send(js)
#     elif isinstance(event, GroupMessageEvent):
#         await send2(js, bot, event)


randomCard = on_command('随机一卡', aliases={'抽一张卡'})


@randomCard.handle()
async def _(bot: Bot, event: Event, state: T_State):
    if isinstance(event, PrivateMessageEvent):
        sessionId = 'user_' + str(event.user_id)
        userType = 'private'
    if isinstance(event, GroupMessageEvent):
        sessionId = 'group_' + str(event.group_id)
        userType = 'group'
    try:
        userType = 'SU' if (str(event.user_id) in nonebot.get_driver().config.superusers) else userType
        pm.CheckPermission(sessionId, userType)
        try:
            url = oriurl + "randomCard"
            result = requests.get(url).text
            js = json.loads(result)
        except Exception as e:
            await randomCard.finish("咿呀？卡组被送进异次元了呢~")
        await send3(js, randomCard)
    except PermissionError as e:
        pass


wm_list = ['同调', '仪式', '融合', '超量', '链接', '灵摆', '顶 G', '重坑', '干饭', '开壶', '唠嗑', '摸鱼']

dailycard = on_command('今日游戏王', aliases={'今日卡运', '今日牌运'})


@dailycard.handle()
async def _(bot: Bot, event: Event, state: T_State):
    # 正常版本
    qq = int(event.get_user_id())
    point = hash(qq)
    daily = int(point)
    daily_point_map = point % 100
    wm_value = []
    lend = len(wm_list)
    for i in range(lend):
        wm_value.append(point & 3)
        point >>= 2
    s = f"今日人品值：{daily_point_map}\n"
    flag = 0
    for i in range(lend):
        if wm_value[i] == 3:
            s += f'宜 {wm_list[i]}'
            if flag % 2 == 0:
                s += '　　'
                flag += 1
            else:
                s += f'\n'
                flag += 1
        elif wm_value[i] == 0:
            s += f'忌 {wm_list[i]}'
            if flag % 2 == 0:
                s += '　　'
                flag += 1
            else:
                s += f'\n'
                flag += 1
        if i == lend - 1 and flag % 2 == 1:
            s += f'\n'
    card = obj[daily % len(obj)]
    s += f'小蓝提醒您：打牌要保持良好心态哟~\n今日{card["type"]}：'
    no = daily % int(card['nums'])
    await dailycard.finish(
        Message([
                    {"type": "text", "data": {"text": s}}
                ] + card_txt(card, no)), at_sender=True)


# ==========各类开关=============================

# 抽卡开关
ckpem = on_command("抽卡功能", permission=GROUP_ADMIN | GROUP_OWNER | SUPERUSER)


@ckpem.handle()
async def cmdArg(bot: Bot, event: Event, state: T_State):
    message = event.get_message()
    if 'off' in str(message):
        state['add_mode'] = True
    elif 'on' in str(message):
        state['add_mode'] = False
    else:
        await ckpem.finish(f'无效参数: {message}, 请输入 on 或 off 为参数')


# 群聊部分自动获取sid
@ckpem.handle()
async def group(bot: Bot, event: GroupMessageEvent, state: T_State):
    state['sid'] = 'group_' + str(event.group_id)
    sid = str(state['sid'])
    if not verifySid(sid):
        await ckpem.reject(f"无效目标对象: {sid}")
    await ckpem.finish(pm.UpdateBanList(sid, state['add_mode']))


# 查卡方式
searchType = on_command("查卡方式")


@searchType.handle()
async def seartype(bot: Bot, event: GroupMessageEvent, state: T_State):
    message = str(event.get_message()).replace(" ", "")
    state['sid'] = 'group_' + str(event.group_id)
    sid = str(state['sid'])
    if message.isdigit():
        if not verifySid(sid):
            await searchType.reject(f"无效目标对象: {sid}")
        await searchType.finish(sm.UpdateSearchType(sid, int(message)))
    else:
        await searchType.finish("请选择正确的方式")




obj = requests.get(oriurl + "searchDaily").json()['data']

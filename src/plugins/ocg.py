import json

import nonebot

from nonebot.permission import SUPERUSER
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Event, Bot, GroupMessageEvent, PrivateMessageEvent, GROUP_ADMIN, \
    GROUP_OWNER
from nonebot import on_command
from src.libraries.searchManage import SearchManager
from src.libraries.sendAction import *
from src.libraries.tool import hash
from src.libraries.permissionManage import PermissionManager

oriurl = "http://ocgcard.fireinsect.top/"
# oriurl = "http://localhost:3399/"
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
async def _(bot: Bot, event: Event, state: T_State):
    if isinstance(event, PrivateMessageEvent):
        sessionId = 'user_' + str(event.user_id)
        userType = 'private'
    if isinstance(event, GroupMessageEvent):
        sessionId = 'group_' + str(event.group_id)
        userType = 'group'
    regex = "(.+) (魔法|怪兽|陷阱)?([0-9]+)?"
    text = str(event.get_message()).strip()
    if text == "":
        await search_card.finish("请输入需要查询的卡名")
    try:
        match = re.match(regex, text)
        if match:
            search_group = match.groups()
        else:
            text += " 1"
            match = re.match(regex, text)
            search_group = match.groups()
        state['name'] = search_group[0]
        state['type'] = search_group[1]
        state['page'] = search_group[2]
        url = oriurl + "getCard?name={0}&type={1}&page={2}".format(search_group[0], search_group[1], search_group[2])
        result = requests.get(url).text
        js = json.loads(result)
    except Exception as e:
        await search_card.finish("咿呀？查询失败了呢")
    if int(search_group[2]) > int(js['data']['pageNum']):
        await search_card.finish("页码超出最大值" + "`" + str(js['data']['pageNum']) + "`")
    state['js'] = js
    if js['data']['amount'] == 0:
        await sendNosearch(search_card)
    elif isinstance(event, PrivateMessageEvent):
        await send2(js, search_card)
    elif isinstance(event, GroupMessageEvent):
        typee = sm.CheckType(sessionId)
        state['send_type'] = typee
        if typee == 1:
            await send2(js, search_card)
        elif typee == 2:
            await send(js, bot, event, search_card)
        else:
            await send3(js, search_card)


@search_card.got("text", prompt="欧尼酱~输入任意语句或选择任意卡牌结束本次查卡~")
async def _(bot: Bot, event: Event, state: T_State):
    text = str(state['text'])
    js = state['js']
    if text.isdigit():
        if isinstance(event, PrivateMessageEvent):
            typee = 1
        elif isinstance(event, GroupMessageEvent):
            typee = int(state['send_type'])
        len = int(js['data']['amount'])
        chose = int(text)
        if 1 <= chose <= len:
            if typee == 1:
                await send2(js, search_card, chose)
            elif typee == 2:
                await send(js, bot, event, search_card, chose)
            else:
                await send3(js, search_card, chose)
    else:
        name = state['name']
        type = state['type']
        page = int(state['page'])
        url = None
        print(text)
        if text == "下一页":
            if page == js['data']['pageNum']:
                await search_card.reject("欧尼酱~已经到最后一页了~")
            else:
                page = page + 1
                url = oriurl + "getCard?name={0}&type={1}&page={2}".format(name, type, page)
                state['page'] = page
        elif text == "上一页":
            if page == 1:
                await search_card.reject("欧尼酱~已经是第一页了~")
            else:
                page = page - 1
                url = oriurl + "getCard?name={0}&type={1}&page={2}".format(name, type, page)
                state['page'] = page
        else:
            await search_card.finish()
        if url is not None:
            print("asdasda")
            result = requests.get(url).text
            js = json.loads(result)
            state['js'] = js
            if js['data']['amount'] == 0:
                await sendNosearch(search_card)
            elif isinstance(event, PrivateMessageEvent):
                await send2(js, search_card)
            elif isinstance(event, GroupMessageEvent):
                typee = state['send_type']
                if typee == 1:
                    await send2(js, search_card)
                elif typee == 2:
                    await send(js, bot, event, search_card)
                else:
                    await send3(js, search_card)
            await search_card.reject("")


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
    groupSession = None
    sessionId = None
    if isinstance(event, PrivateMessageEvent):
        sessionId = 'user_' + str(event.user_id)
        userType = 'private'
    if isinstance(event, GroupMessageEvent):
        groupSession = 'group_' + str(event.group_id)
        sessionId = 'user_' + str(event.sender.user_id)
        userType = 'group'
    try:
        userType = 'SU' if (str(event.user_id) in nonebot.get_driver().config.superusers) else userType
        pm.CheckPermission(sessionId, groupSession, userType)
    except PermissionError as e:
        await randomCard.finish(str(e))
    try:
        url = oriurl + "randomCard"
        result = requests.get(url).text
        js = json.loads(result)
        pm.UpdateLastSend(sessionId)
    except Exception as e:
        await randomCard.finish("咿呀？卡组被送进异次元了呢~")
    await send3(js, randomCard)


# ==========各类开关=============================

# ----- 抽卡cd时间更新 -----
random_cd = on_command("抽卡cd", permission=GROUP_ADMIN | GROUP_OWNER | SUPERUSER, block=True, priority=10)


# 获取参数
@random_cd.handle()
async def cmdArg(bot: Bot, event: Event, state: T_State):
    message = str(event.get_message()).replace(" ", "")
    try:
        state['cdTime'] = int(str(message))
    except:
        await random_cd.finish(f'无效参数: {message}, 请输入 正整数 或 0 为参数')


# 群聊部分自动获取sid
@random_cd.handle()
async def group(bot: Bot, event: GroupMessageEvent, state: T_State):
    sid = 'group_' + str(event.group_id)
    if not verifySid(sid):
        await random_cd.reject(f"无效目标对象: {sid}")
    await random_cd.finish(pm.UpdateCd(sid, state['cdTime']))


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

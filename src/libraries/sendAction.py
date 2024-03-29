import random
import re

import requests
from nonebot.adapters.cqhttp import Message

from src.libraries.globalMessage import noSearchText, lanName
from src.libraries.image import *

static_url = "http://fireinsect.top/ocgBot/ocg-bot/src/static/pics/"
# 缩放比例
PANTOGRAPH = 0.6

def getResult(car):
    result = ""
    result += car['name'] + "\n" + car['type'] + "\nid-" + str(car['cardId']) + " " + car[
        'forbidden'] + "\n\n"
    car['effect'] = car['effect'].replace('\r', '')
    if car['mainType'] == '怪兽':
        if car['atk'] == "-2":
            car['atk'] = '?'
        if car['def'] == "-2":
            car['def'] = '?'

        if car['def'] is None:
            result += car['level'] + ' / ' + car[
                'zz'] + ' / ' + car['attribute'] + "\n" + 'ATK:' + car['atk'] + "\n\n"
        else:
            result += car['level'] + ' / ' + car[
                'zz'] + ' / ' + car['attribute'] + "\n" + 'ATK:' + car['atk'] + ' / DEF:' + car['def'] + "\n\n"
        # car['effect'] = re.sub(r"(.{50})", "\\1\n", car['effect'])
        result += car['effect']
    else:
        # car['effect'] = re.sub(r"(.{50})", "\\1\n", car['effect'])
        result += car['effect']
    return result


def card_txt(card, no):
    return Message([
        {
            "type": "text",
            "data": {
                "text": f"{card['id']}. {card['name']}-{no + 1}\n"
            }
        },
        {
            "type": "image",
            "data": {
                "file": f"http://ocgcard.daily.fireinsect.top/deck/{card['id']}/{card['id']}-{no}.jpg"
            }
        }
    ])


async def sendNosearch(func):
    r = random.randint(0, len(noSearchText) - 1)
    await func.finish(noSearchText[r])


# ==========发送方式=============================
# 合并消息方式
async def send(js, bot, event, func, num=0):
    if js['data']['amount'] == 0:
        sendNosearch(func)
    else:
        msg_list = []
        pics_url = static_url + str(
            js['data']['cards'][0]['cardId']) + '.jpg'
        if num != 0:
            num = num - 1
            pics_url = static_url + str(
                js['data']['cards'][num]['cardId']) + '.jpg'
            if img_exist(pics_url):
                messageListAppend(js, pics_url, num, msg_list)
        elif js['data']['amount'] == 1 and img_exist(pics_url):
            messageListAppend(js, pics_url, num, msg_list)
        else:
            messageListCreate(js, msg_list)
    msgs = []
    r = random.randint(0, len(lanName) - 1)
    for msg in msg_list:
        msgs.append({
            'type': 'node',
            'data': {
                'name': lanName[r],
                'uin': bot.self_id,
                'content': msg
            }
        })
    await bot.call_api('send_group_forward_msg', group_id=event.group_id, messages=msgs)
    if js['data']['amount'] == 1:
        await func.finish()


# 出现完整效果的方式
async def send2(js, func, num=0):
    pics_url = static_url + str(
        js['data']['cards'][0]['cardId']) + '.jpg'
    if js['data']['amount'] == 0:
        sendNosearch(func)
    # num!=0即用户选择详细卡牌信息
    elif num != 0:
        num = num - 1
        pics_url = static_url + str(
            js['data']['cards'][num]['cardId']) + '.jpg'
        if img_exist(pics_url):
            await func.finish(getAllMessage(js, pics_url, num))
    elif js['data']['amount'] == 1 and img_exist(pics_url):
        await func.finish(getAllMessage(js, pics_url, num))
    else:
        await send_cards_byCard(js, func)


# 单卡图方式
async def send3(js, func, num=0):
    pics_url = static_url + str(
        js['data']['cards'][0]['cardId']) + '.jpg'
    if js['data']['amount'] == 0:
        sendNosearch(func)
    # num!=0即用户选择详细卡牌信息
    elif num != 0:
        num = num - 1
        pics_url = static_url + str(
            js['data']['cards'][num - 1]['cardId']) + '.jpg'
        if img_exist(pics_url):
            await func.finish(getPicOnlyMessage(js, num, pics_url))
    elif js['data']['amount'] == 1 and img_exist(pics_url):
        await func.finish(getPicOnlyMessage(js, num, pics_url))
    else:
        await send_cards_byCard(js, func)


# ===========用于进行Message和合并消息的合成=================
# 提供给合并格式的单卡
def messageListAppend(js, url, num, msg_list):
    car = js['data']['cards'][num]
    img = Image.open(BytesIO(requests.get(url).content))
    msg_list.append(Message([
        {
            "type": "image",
            "data": {
                # "file": f"base64://{str(image_to_base64(Image.open('src/static/pics/' + str(js['data'][
                # 'cards'][0]['cardId']) + '.jpg')), encoding='utf-8')}"
                "file": f"base64://{str(image_to_base64(img.resize((int(img.size[0] * PANTOGRAPH), int(img.size[1] * PANTOGRAPH)), Image.ANTIALIAS)), encoding='utf-8')}"}
        }
    ]))
    msg_list.append(Message([
        {
            "type": "text",
            "data": {
                "text": getResult(car)
            }
        },
    ]))


# 提供给合并格式的多卡结果
def messageListCreate(js, msg_list):
    for car in js['data']['cards']:
        msg_list.append(Message([
            {
                "type": "text",
                "data": {
                    "text": getResult(car)
                }
            },
        ]))
    msg_list.append(Message([
        {
            "type": "text",
            "data": {
                "text": f"欧尼酱！找到了{js['data']['amount']}张卡哟~,当前{js['data']['nowNum']}/{js['data']['pageNum']}页"
            }
        },
    ]))
    msg_list.append(Message([
        {
            "type": "text",
            "data": {
                "text": f"考虑到图片发送问题，只有查到一张卡的时候才会发送卡图哟~"
            }
        },
        {
            "type": "text",
            "data": {
                "text": f"输入数字可以选择搜索结果捏！"
            }
        }
    ]))


# 获取完整效果形式的Message
def getAllMessage(js, url, num):
    car = js['data']['cards'][num]
    img = Image.open(BytesIO(requests.get(url).content))
    return Message([
        {
            "type": "image",
            "data": {
                # "file": f"base64://{str(image_to_base64(Image.open('src/static/pics/' + str(js['data'][
                # 'cards'][0]['cardId']) + '.jpg')), encoding='utf-8')}"
                "file": f"base64://{str(image_to_base64(img.resize((int(img.size[0] * PANTOGRAPH), int(img.size[1] * PANTOGRAPH)), Image.ANTIALIAS)), encoding='utf-8')}"
            }
        },
        {
            "type": "text",
            "data": {
                "text": getResult(car)
            }
        },
    ])


# 获取单卡图形式的Message
def getPicOnlyMessage(js, num, url):
    return Message([
        {
            "type": "text",
            "data": {
                "text": f"卡片id:{js['data']['cards'][num]['cardId']}  {js['data']['cards'][num]['forbidden']}\n {js['data']['cards'][num]['name']}\n"
                # f"jp:{js['data']['cards'][0]['jpName']}\n"
                # f"en:{js['data']['cards'][0]['enName']}\n"
            }
        },
        {
            "type": "image",
            "data": {
                # "file": f"base64://{str(image_to_base64(Image.open('src/static/pics/' + str(js['data'][
                # 'cards'][0]['cardId']) + '.jpg')), encoding='utf-8')}"
                "file": f"base64://{str(image_to_base64(Image.open(BytesIO(requests.get(url).content))), encoding='utf-8')}"
            }
        }
    ])


# =========判断============
# 判断图片是否存在
def img_exist(url):
    return requests.head(url).status_code == requests.codes.ok
# =====================

# 图片形式发送多张卡
async def send_cards_byCard(js, func):
    result = ""
    for car in js['data']['cards']:
        result += car['name'] + "     " + car['type'] + "    id-" + str(car['cardId']) + "    " + car[
            'forbidden'] + "\n"
        if car['enName'] is not None:
            result += "英文卡名-" + car['enName'] + "     " + "日文卡名-" + car['jpName'] + "\n"
        car['effect'] = car['effect'].replace('\r', '')
        if car['mainType'] == '怪兽':
            if car['atk'] == "-2":
                car['atk'] = '?'
            if car['def'] == "-2":
                car['def'] = '?'

            if car['def'] is None:
                result += car['level'] + ' / ATK: ' + car['atk'] + ' / : ' + car[
                    'zz'] + ' / ' + car['attribute'] + "\n"
            else:
                result += car['level'] + ' / ATK: ' + car['atk'] + ' / DEF: ' + car['def'] + ' / : ' + car[
                    'zz'] + ' / ' + car['attribute'] + "\n"
            car['effect'] = re.sub(r"(.{50})", "\\1\n", car['effect'])
            result += "效果：" + car['effect'] + "\n"
            result += "\n"
            result += "\n"
        else:
            car['effect'] = re.sub(r"(.{50})", "\\1\n", car['effect'])
            result += "效果：" + car['effect'] + "\n"
            result += "\n"
            result += "\n"

    page_text = str.format("找到了{0}张卡哟~,当前{1}/{2}页     输入数字可以选择搜索结果！输入`上一页`/`下一页` 进行翻页~", js['data']['amount'], js['data']['nowNum'],
                           js['data']['pageNum'])
    await func.send(Message([{
        "type": "image",
        "data": {
            "file": f"base64://{str(image_to_base64(text_to_image2(result, page_text)), encoding='utf-8')}"
        }
    }]))

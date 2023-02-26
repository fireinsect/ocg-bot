import random
import re

import requests
from nonebot.adapters.cqhttp import Message

from src.libraries.image import *


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


# 缩放比例
PANTOGRAPH = 0.6

noSearchText = [
    "没找到捏~ 欧尼酱~",
    "咦？这张卡不存在呢",
    "哔哔~卡片不存在"
]

lanName = [
    "今天有没有好好打牌呢？",
    "适度打牌，注意休息",
    "废物小蓝，嗷呜嗷呜",
    "可可爱爱，没有脑袋",
    "小蓝(洗衣服ing)",
    "你看你脏的，让我洗！",
    "呜，不会打牌唔",
    "摸鱼的G",
    "小蓝(非卖品)",
    "今天堆点什么捏?",
    "嘟嘟嘟，小蓝警长"
]


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
        pics_url = 'http://fireinsect.top/ocgBot/ocg-bot/src/static/pics/' + str(
            js['data']['cards'][0]['cardId']) + '.jpg'
        if num != 0:
            num = num - 1
            pics_choose_url = 'http://fireinsect.top/ocgBot/ocg-bot/src/static/pics/' + str(
                js['data']['cards'][num]['cardId']) + '.jpg'
            if requests.head(pics_choose_url).status_code == requests.codes.ok:
                car = js['data']['cards'][num - 1]
                img = Image.open(BytesIO(requests.get(pics_choose_url).content))
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
        elif js['data']['amount'] == 1 and requests.head(pics_url).status_code == requests.codes.ok:
            car = js['data']['cards'][0]
            img = Image.open(BytesIO(requests.get(pics_url).content))
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
        else:
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
    pics_url = 'http://fireinsect.top/ocgBot/ocg-bot/src/static/pics/' + str(
        js['data']['cards'][0]['cardId']) + '.jpg'
    if js['data']['amount'] == 0:
        sendNosearch(func)
    elif num != 0:
        num = num - 1
        pics_choose_url = 'http://fireinsect.top/ocgBot/ocg-bot/src/static/pics/' + str(
            js['data']['cards'][num]['cardId']) + '.jpg'
        if requests.head(pics_choose_url).status_code == requests.codes.ok:
            car = js['data']['cards'][num]
            img = Image.open(BytesIO(requests.get(pics_choose_url).content))
            await func.finish(Message([
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
            ]))
    elif js['data']['amount'] == 1 and requests.head(pics_url).status_code == requests.codes.ok:
        car = js['data']['cards'][0]
        img = Image.open(BytesIO(requests.get(pics_url).content))
        await func.finish(Message([
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
        ]))
    else:
        await send_cards_byCard(js,func)


# 单卡图方式
async def send3(js, func, num=0):
    pics_url = 'http://fireinsect.top/ocgBot/ocg-bot/src/static/pics/' + str(
        js['data']['cards'][0]['cardId']) + '.jpg'
    if js['data']['amount'] == 0:
        sendNosearch(func)
    elif num != 0:
        num = num - 1
        pics_choose_url = 'http://fireinsect.top/ocgBot/ocg-bot/src/static/pics/' + str(
            js['data']['cards'][num]['cardId']) + '.jpg'
        if requests.head(pics_choose_url).status_code == requests.codes.ok:
            await func.finish(Message([
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
                        "file": f"base64://{str(image_to_base64(Image.open(BytesIO(requests.get(pics_choose_url).content))), encoding='utf-8')}"
                    }
                }
            ]))

    elif js['data']['amount'] == 1 and requests.head(pics_url).status_code == requests.codes.ok:
        await func.finish(Message([
            {
                "type": "text",
                "data": {
                    "text": f"卡片id:{js['data']['cards'][0]['cardId']}  {js['data']['cards'][0]['forbidden']}\n {js['data']['cards'][0]['name']}\n"
                    # f"jp:{js['data']['cards'][0]['jpName']}\n"
                    # f"en:{js['data']['cards'][0]['enName']}\n"
                }
            },
            {
                "type": "image",
                "data": {
                    # "file": f"base64://{str(image_to_base64(Image.open('src/static/pics/' + str(js['data'][
                    # 'cards'][0]['cardId']) + '.jpg')), encoding='utf-8')}"
                    "file": f"base64://{str(image_to_base64(Image.open(BytesIO(requests.get(pics_url).content))), encoding='utf-8')}"
                }
            }
        ]))
    else:
        await send_cards_byCard(js,func)

#图片形式发送多张卡
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

    page_text = str.format("找到了{0}张卡哟~,当前{1}/{2}页     输入数字可以选择搜索结果捏！", js['data']['amount'], js['data']['nowNum'],
                           js['data']['pageNum'])
    await func.send(Message([{
        "type": "image",
        "data": {
            "file": f"base64://{str(image_to_base64(text_to_image2(result, page_text)), encoding='utf-8')}"
        }
    }]))

import os
import random
import re
import json
import requests

from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Message, Event, Bot
from nonebot import on_command, on_regex
from src.libraries.image import *

# oriurl = "http://ocgcard.fireinsect.top/"
oriurl= "http://localhost:3399/"

noSearchText = [
    "没找到捏~ 欧尼酱~",
    "咦？这张卡不存在呢",
    "哔哔~卡片不存在"
]

search_card = on_regex(r"^查卡.+")


@search_card.handle()
async def _(bot: Bot, event: Event, state: T_State):
    print("start")
    regex = "查卡 (.+) (page)?([0-9]+)?"
    text = event.get_message()
    search_group = re.match(regex, str(text))
    try:
        print(search_group.groups()[2])
    except Exception as e:
        text = text + " page1"
        search_group = re.match(regex, str(text))
        print(search_group.groups()[2])
    try:
        name = search_group.groups()[0]
        page = search_group.groups()[2]
        url = oriurl + "getCard?name=" + name + "&page=" + page
        result = requests.get(url).text
        js = json.loads(result)
    except Exception as e:
        await search_card.send("咿呀？查询失败了呢")
    await send(js)


id_card = on_regex(r"^查id.+")


@id_card.handle()
async def _(bot: Bot, event: Event, state: T_State):
    print("start2")
    regex = "查id ([0-9]+)"
    text = event.get_message()
    search_group = re.match(regex, str(text))
    try:
        id = search_group.groups()[0]
        url = oriurl + "searchCardId?cardId=" + id
        result = requests.get(url).text
        js = json.loads(result)
    except Exception as e:
        await search_card.send("咿呀？查询失败了呢")
    await send(js)

randomCard = on_command('随机一卡', aliases={'抽一张卡'})
@randomCard.handle()
async def _(bot: Bot, event: Event, state: T_State):
    try:
        url = oriurl + "randomCard"
        result = requests.get(url).text
        js = json.loads(result)
    except Exception as e:
        await search_card.send("咿呀？卡组被送进异次元了呢~")
    await send(js)

async def send(js):
    result = ""
    if js['data']['amount'] == 0:
        r = random.randint(0, len(noSearchText) - 1)
        await search_card.send(noSearchText[r])
    else:
        for car in js['data']['cards']:
            car['effect'] = car['effect'].replace('\r', '')
            if car['mainType'] == '怪兽':
                if car['atk'] == "-2":
                    car['atk'] = '?'
                if car['def'] == "-2":
                    car['def'] = '?'
                result += car['name'] + "     " + car['type'] + "    id-" + str(car['cardId']) + "\n"
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

                result += car['name'] + "     " + car['type'] + "    id-" + str(car['cardId']) + "\n"
                car['effect'] = re.sub(r"(.{50})", "\\1\n", car['effect'])
                result += "效果：" + car['effect'] + "\n"
                result += "\n"
                result += "\n"
        if js['data']['amount'] == 1 and os.path.exists(
                'src/static/pics/' + str(js['data']['cards'][0]['cardId']) + '.jpg'):

            await search_card.finish(Message([
                {
                    "type": "text",
                    "data": {
                        "text": f"卡片id:{js['data']['cards'][0]['cardId']}\n {js['data']['cards'][0]['name']}\n"
                    }
                },
                {
                    "type": "image",
                    "data": {
                        "file": f"base64://{str(image_to_base64(Image.open('src/static/pics/' + str(js['data']['cards'][0]['cardId']) + '.jpg')), encoding='utf-8')}"
                    }
                }
            ]))
        else:
            page_text = str.format("找到了{0}张卡哟~,当前{1}/{2}页", js['data']['amount'], js['data']['nowNum'],
                                   js['data']['pageNum'])
            await search_card.finish(Message([{
                "type": "image",
                "data": {
                    "file": f"base64://{str(image_to_base64(text_to_image2(result, page_text)), encoding='utf-8')}"
                }
            }]))

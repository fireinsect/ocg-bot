import os
import random
import re
import json
import requests
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Message, Event, Bot
from nonebot import on_command, on_regex
from src.libraries.image import *
from src.libraries.raiseCard import draw_card_text
from src.libraries.tool import hash

oriurl = "http://ocgcard.fireinsect.top/"
# oriurl = "http://localhost:3399/"

noSearchText = [
    "没找到捏~ 欧尼酱~",
    "咦？这张卡不存在呢",
    "哔哔~卡片不存在"
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


ocghelp = on_command('ygo help', aliases={'ygo 帮助', 'ygohelp', 'ygo帮助'})


@ocghelp.handle()
async def _(bot: Bot, event: Event, state: T_State):
    txt = '''欧尼酱~你可以对查卡姬说如下命令哟~
    随机一卡(抽一张卡)
    今日卡运   查看今天打牌运势~
    查卡 ygo卡名 (怪兽|魔法|陷阱) (页码)   查询对应卡牌~
    en查卡(英文查卡) 英文卡名 (页码)   使用英文查询对应卡牌~
    查id 卡片id   查询对应id~'''
    await ocghelp.send(Message([{
        "type": "image",
        "data": {
            "file": f"base64://{str(image_to_base64(text_to_image(txt)), encoding='utf-8')}"
        }
    }]))


ensearch_card = on_command("en查卡 ", aliases={'英文查卡 '})


@ensearch_card.handle()
async def _(bot: Bot, event: Event, state: T_State):
    text = event.get_message()
    regex = "(.+) (page)?([0-9]+)?"
    search_group = re.match(regex, str(text))
    try:
        print(search_group.groups()[2])
    except Exception as e:
        text = text + " 1"
        search_group = re.match(regex, str(text))
    try:
        if search_group.groups()[2] is None:
            text = text + " 1"
            search_group = re.match(regex, str(text))
        name = search_group.groups()[0]
        page = search_group.groups()[2]
        url = oriurl + "getCardByEn?enName=" + name + "&page=" + page
        result = requests.get(url).text
        js = json.loads(result)
    except Exception as e:
        await ensearch_card.send("咿呀？查询失败了呢")
    await send(js)


search_card = on_command("查卡 ")


@search_card.handle()
async def _(bot: Bot, event: Event, state: T_State):
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
        print(name)
        print(url)
        result = requests.get(url).text
        js = json.loads(result)
    except Exception as e:
        await search_card.send("咿呀？查询失败了呢")
    await send(js)


id_card = on_command("查id ")


@id_card.handle()
async def _(bot: Bot, event: Event, state: T_State):
    regex = "([0-9]+)"
    text = str(event.get_message()).strip()
    search_group = re.match(regex, text)
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
        pics_url = 'http://fireinsect.top/ocgBot/ocg-bot/src/static/pics/' + str(
            js['data']['cards'][0]['cardId']) + '.jpg'
        # if js['data']['amount'] == 1 and os.path.exists('src/static/pics/' + str(js['data']['cards'][0]['cardId'])
        # + '.jpg'):
        if js['data']['amount'] == 1 and requests.head(pics_url).status_code == requests.codes.ok:

            await search_card.finish(Message([
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
            page_text = str.format("找到了{0}张卡哟~,当前{1}/{2}页", js['data']['amount'], js['data']['nowNum'],
                                   js['data']['pageNum'])
            await search_card.finish(Message([{
                "type": "image",
                "data": {
                    "file": f"base64://{str(image_to_base64(text_to_image2(result, page_text)), encoding='utf-8')}"
                }
            }]))


wm_list = ['同调', '仪式', '融合', '超量', '链接', '灵摆', '顶 G', '重坑', '干饭', '开壶', '唠嗑', '摸鱼']

dailycard = on_command('今日游戏王', aliases={'今日卡运', '今日牌运'})


@dailycard.handle()
async def _(bot: Bot, event: Event, state: T_State):
    # 520专属
    # s = f"今日人品值：-999\n"
    # s += f'忌 出游\n'
    # s += f'忌 同行\n'
    # s += f'忌 520\n'
    # s += f'忌 秀恩爱\n'
    # s += f'忌 抛洒狗粮\n'
    # s += f'宜 打牌（人品值+1099）\n'
    # s += f"小虫告诉您：今天就适合打牌 我说的！\n今日卡牌："
    # card = {
    #     'id': 114514,
    #     'name': "废物"
    # }
    # await dailycard.finish(
    #     Message([
    #                 {"type": "text", "data": {"text": s}}
    #             ] + card_txt(card)), at_sender=True)

    # 端午版
    # qq = int(event.get_user_id())
    # point = hash(qq)
    # daily_point_map = point % 100
    # if daily_point_map < 10:
    #     daily_point_map += 60
    # elif daily_point_map < 30:
    #     daily_point_map += 40
    # elif daily_point_map < 50:
    #     daily_point_map += 20
    # wm_value = []
    # lend = len(wm_list)
    # for i in range(lend):
    #     wm_value.append(point & 2)
    #     point >>= 2
    # s = f"今日人品值：{daily_point_map}\n"
    # for i in range(lend):
    #     if wm_value[i] == 2:
    #         s += f'宜 {wm_list[i]}\n'
    # s += f'宜 吃粽子\n'
    # if hash(qq)%150>145:
    #     s += f'宜 找查卡姬唠\n'
    # card = obj[point % len(obj)]
    # s += f"今天是端午节哟，快快乐乐才是最重要哒！\n今日{card['type']}："

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
    s += f'小虫提醒您：打牌要保持良好心态哟\n今日{card["type"]}：'
    no = daily % int(card['nums'])
    await dailycard.finish(
        Message([
                    {"type": "text", "data": {"text": s}}
                ] + card_txt(card, no)), at_sender=True)




obj = requests.get(oriurl + "searchDaily").json()['data']

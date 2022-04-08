import re
import json
import requests


from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Message, Event, Bot
from nonebot import on_command, on_regex
from src.libraries.image import *

search_card = on_regex(r"查卡.+")

@search_card.handle()
async def _(bot: Bot, event: Event, state: T_State):
    print("start")
    oriurl= "http://ocgcard.fireinsect.top/getCard?name="
    # oriurl= "http://localhost:3399/getCard?name="
    regex = "查卡 (.+) (page)?([0-9]+)?"
    text=event.get_message()
    search_group = re.match(regex,str(text))
    try:
        print(search_group.groups()[2])
    except Exception as e:
        text=text+" page1"
        search_group = re.match(regex, str(text))
        print(search_group.groups()[2])
    try:
        name = search_group.groups()[0]
        page = int(search_group.groups()[2])
        if (page == None):
            url = oriurl + search_group.groups()[0]
        else:
            url = oriurl + search_group.groups()[0] + "&page=" + search_group.groups()[2]
        result = requests.get(url).text
        js=json.loads(result)
        result = ""
    except Exception as e:
        await search_card.send("查询失败")
    if(js['data']['amount']==0):
        await search_card.send("没找到捏~ 欧尼")
    else:
        for car in js['data']['cards']:
            if car['mainType'] == '怪兽':
                result += car['name'] + "     " + car['type'] + "\n"
                if(car['def']==None):
                    result += car['level'] + ' / ATK: ' + car['atk'] + ' / : ' + car[
                        'zz'] + ' / ' + car['attribute'] + "\n"
                else:
                    result += car['level'] + ' / ATK: ' + car['atk'] + ' / DEF: ' + car['def'] + ' / : ' + car[
                        'zz'] + ' / ' + car['attribute'] + "\n"
                car['effect'] = re.sub(r"(.{50})", "\\1\r\n", car['effect'])
                result += "效果：" + car['effect'] + "\n"
                result += "\n"
                result += "\n"
            else:

                result += car['name'] + "     " + car['type'] + "\n"
                car['effect'] = re.sub(r"(.{50})", "\\1\r\n", car['effect'])
                result += "效果：" + car['effect'] + "\n"
                result += "\n"
                result += "\n"
        page_text = str.format("找到了{0}张卡哟~,当前{1}/{2}页",js['data']['amount'],js['data']['nowNum'],js['data']['pageNum'])
        await search_card.finish(Message([{
            "type": "image",
            "data": {
                "file": f"base64://{str(image_to_base64(text_to_image2(result,page_text)), encoding='utf-8')}"
            }
        }]))


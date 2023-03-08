import re
import requests
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Event, Bot, Message
from nonebot import on_command

from src.libraries.image import image_to_base64, text_to_image2, text_to_image_with_back

gradeUrl = "https://api.jihuanshe.com/api/market/search/match-product?game_key=ygo&game_sub_key=ocg&type=card_version"

priceSearch = on_command('集换社查询', aliases={'价格查询'})


@priceSearch.handle()
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
        name = textNext
        url = gradeUrl + "&keyword={0}&page={1}".format(name, page)
        result = requests.get(url).json()
        page_text = "找到了{0}条数据哟~,当前{1}/{2}页 数据来源：集换社".format(result['total'], result['current_page'],
                                                             result['last_page'])

        await priceSearch.send(Message([{
            "type": "image",
            "data": {
                "file": f"base64://{str(image_to_base64(text_to_image_with_back(getPriceStr(result), page_text, '价格表')), encoding='utf-8')}"
            }
        }]))
    except Exception as e:
        e.with_traceback()
        await priceSearch.finish("咿呀？查询失败了呢")


def getPriceStr(json):
    result = ""
    for item in json['data']:
        result += "{0} {1}   {4}￥起 \n名称：{2} {3} \n\n".format(item['number'], item['rarity'], item['name_cn'],
                                                             item['name_origin'], item['min_price'])
    return result

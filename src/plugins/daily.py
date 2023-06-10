import datetime
from io import BytesIO

import requests
from PIL import Image, ImageFont, ImageDraw
from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, Event,Message
from nonebot.typing import T_State

from src.libraries.image import image_to_base64
from src.libraries.sendAction import card_txt

wm_list = ['同调', '仪式', '融合', '超量', '链接', '灵摆', '顶 G', '重坑', '干饭', '开壶', '唠嗑', '摸鱼']
dailycard = on_command('今日游戏王', aliases={'今日卡运', '今日牌运'})
oriurl = "http://ocgcard.fireinsect.top/"
obj = requests.get(oriurl + "searchDaily").json()['data']
lend = len(wm_list)


@dailycard.handle()
async def _(bot: Bot, event: Event, state: T_State):
    # 正常版本
    qq = int(event.get_user_id())
    point = int(hash(qq))
    wm_value = []
    for i in range(lend):
        wm_value.append(point & 3)
        point >>= 2
    await dailycard.finish(getDailyPic(point, wm_value), at_sender=True)


def getDailyPic(point: int, wm_value):
    card = obj[point % len(obj)]
    no = point % int(card['nums'])
    if card['type'] == "系列":
        back_pic = Image.open("src/static/daily_xilie.png")
    else:
        back_pic = Image.open("src/static/daily_kapai.png")
    url = f"http://ocgcard.daily.fireinsect.top/deck/{card['id']}/{card['id']}-{no}.jpg"
    cardPic = Image.open(BytesIO(requests.get(url).content))
    proper_list = []
    envy_list = []
    for i in range(lend):
        if wm_value[i] == 3:
            proper_list.append(wm_list[i])
        elif wm_value[i] == 0:
            envy_list.append(wm_list[i])
    weekday = datetime.datetime.now().weekday()
    daily = point % 100
    card_str = f"{card['name']}-{no + 1}"
    extra_text = "小蓝提醒您：打牌要保持良好心态哟~"
    pic_joint(back_pic, cardPic, daily, extra_text, weekday, card_str, proper_list, envy_list)
    return Message([{
            "type": "image",
            "data": {
                "file": f"base64://{str(image_to_base64(back_pic), encoding='utf-8')}"
            }
    }])


def getDailyText(point: int, wm_value):
    daily = point % 100
    s = f"今日人品值：{daily}\n"
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
    card = obj[point % len(obj)]
    s += f'小蓝提醒您：打牌要保持良好心态哟~\n今日{card["type"]}：'
    no = point % int(card['nums'])
    return Message([
                       {"type": "text", "data": {"text": s}}
                   ] + card_txt(card, no))


# ---图片拼接---
font_path = "src/static/msyh.ttc"
fontWeek = ImageFont.truetype(font_path, 35)
fontList = ImageFont.truetype(font_path, 25)
fontCardStr = ImageFont.truetype(font_path, 28)
fontText = ImageFont.truetype(font_path, 28)
fontPoint = ImageFont.truetype(font_path, 50)


def pic_joint(backPic: Image, cardPic: Image, daily: int, extra_text: str, weekday: int, card_str: str, proper_list,
              envy_list):
    draw = ImageDraw.Draw(backPic)
    num_dict = {"0": u"一", "1": u"二", "2": u"三", "3": u"四", "4": u"五", "5": u"六", "6": u"日"}
    week = f"星期{num_dict.get(str(weekday))}"
    draw.text((550, 50), week, font=fontWeek, fill=(92, 128, 160))
    for i in range(len(proper_list)):
        draw.text((60 + i % 3 * 102, 325 + int(i / 3) * 40), proper_list[i], font=fontList, fill=(92, 128, 160))
    for i in range(len(envy_list)):
        draw.text((60 + i % 3 * 102, 505 + int(i / 3) * 40), envy_list[i], font=fontList, fill=(92, 128, 160))
    draw.text(((backPic.width - fontText.size * len(extra_text)) / 2, 690), extra_text, font=fontText,
              fill=(92, 128, 160))
    backPic.paste(cardPic.resize((280, 280)), (460, 290))
    draw.text((430 + (360-fontCardStr.size * len(card_str)) / 2, 580), card_str, font=fontCardStr, fill=(92, 128, 160))
    draw.text((255, 205), str(daily), font=fontPoint, fill=(92, 128, 160))

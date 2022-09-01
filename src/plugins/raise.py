import os.path

import requests
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Message, Event, Bot, MessageSegment, GroupRequestEvent, GroupMessageEvent
from nonebot import on_command ,on_request
import re
from src.libraries.image import *
from src.libraries.raiseCard import draw_card_text

jupai = on_command("举牌 ", aliases={"我要粉 ", "我要举牌 ", "粉 "})


@jupai.handle()
async def _(bot: Bot, event: Event, state: T_State, ):
    text = str(event.get_message())
    if int(event.get_user_id()) == 847954981:
        await jupai.send(Message([{
            "type": "image",
            "data": {
                "file": f"base64://{str(image_to_base64(draw_card_text(text, 2)), encoding='utf-8')}"
            }
        }]))
    else:
        await jupai.send(Message([{
            "type": "image",
            "data": {
                "file": f"base64://{str(image_to_base64(draw_card_text(text, 1)), encoding='utf-8')}"
            }
        }]))


text = on_command('test')

bieming = on_command("别名收集计划")


@bieming.handle()
async def _(bot: Bot, event: Event, state: T_State, ):
    await bieming.finish(Message([{
        "type": "text",
        "data": {
            "text": f"加入别名收集计划--https://docs.qq.com/sheet/DTWR4bXltbmZiRHdy\n"
        }
    }]))
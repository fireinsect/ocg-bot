import requests
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Message, Event, Bot, MessageSegment
from nonebot import on_command
from src.libraries.image import *
from src.libraries.raiseCard import draw_card_text

jupai = on_command("举牌 ", aliases={"我要粉 ", "我要举牌 ", "粉 "})


@jupai.handle()
async def _(bot: Bot, event: Event, state: T_State, ):
    text = str(event.get_message())
    await jupai.finish(Message([{
        "type": "image",
        "data": {
            "file": f"base64://{str(image_to_base64(draw_card_text(text,1)), encoding='utf-8')}"
        }
    }]))

jupai = on_command("举花牌 ", aliases={"我要狂粉 ", "狂粉 "})


@jupai.handle()
async def _(bot: Bot, event: Event, state: T_State, ):
    if(int(event.get_user_id())==847954981):
        text = str(event.get_message())
        await jupai.finish(Message([{
            "type": "image",
            "data": {
                "file": f"base64://{str(image_to_base64(draw_card_text(text,2)), encoding='utf-8')}"
            }
        }]))

text = on_command('test')


@text.handle()
async def _(bot: Bot, event: Event, state: T_State):
    # id=41
    # await text.send(Message([{
    #     "type": "image",
    #     "data": {
    #         "file": f"http://ocgcard.daily.fireinsect.top/dailycard/41.jpg"
    #     }
    # }]))
    print(event.get_message)
    print(type(event))
    a=event
    print(event.to_me)


import json
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Message, Event, Bot, GroupMessageEvent, PrivateMessageEvent, GROUP_ADMIN, \
    GROUP_OWNER
from nonebot import on_command

fakeMessage = on_command("伪造")


@fakeMessage.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    messages = event.message
    at_message = None
    for meg in messages:
        if meg.type == "at":
            at_message = meg
            messages.remove(meg)
    if at_message is not None:
        msg_gr = []
        to_at=await bot.call_api('get_group_member_info', group_id=event.group_id, user_id=at_message.data['qq'])
        print(to_at)
        if to_at['card'] != "":
            name = to_at['card']
        else:
            name = to_at['nickname']
        msg_gr.append({
            'type': 'node',
            'data': {
                'name': name,
                'uin': at_message.data['qq'],
                'content': messages
            }
        })
        if len(messages)==0:
            await fakeMessage.finish("请输入语句")
        else:
            await bot.call_api('send_group_forward_msg', group_id=event.group_id, messages=msg_gr)
    else:
        await fakeMessage.finish("请选择对象")

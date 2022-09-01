from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Event, Bot
from nonebot.adapters.cqhttp.event import GroupRequestEvent, GroupIncreaseNoticeEvent
from nonebot import on_request, on_notice

addGroupId = 0
addGroupRequestTime = 0

jiaqunRe = on_request()


@jiaqunRe.handle()
async def _(bot: Bot, event: GroupRequestEvent):
    global addGroupId, addGroupRequestTime
    addGroupId = event.group_id
    addGroupRequestTime = event.time


jiaqunNo = on_notice()


@jiaqunNo.handle()
async def _(bot: Bot, event: GroupIncreaseNoticeEvent):
    if event.group_id == addGroupId:
        if event.time == addGroupRequestTime or event.time <= addGroupRequestTime + 7:
            await jiaqunNo.send("检测到非同意拉群")
            await jiaqunNo.send("已退出群聊")
            await bot.set_group_leave(group_id=event.group_id,is_dismiss=False,self_id=bot.self_id)

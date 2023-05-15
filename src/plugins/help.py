from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Event, Bot,Message
from nonebot import on_command

from src.libraries.image import *

ocghelp = on_command('ygo help', aliases={'ygohelp', 'ygo帮助', '#帮助', 'y帮助', '.help', 'yhelp', '#菜单', '菜单', 'help'})


@ocghelp.handle()
async def _(bot: Bot, event: Event, state: T_State):
    txt = '''欧尼酱~你可以对查卡姬说如下命令哟~
    随机一卡(抽一张卡)
    猜一张卡   猜卡游戏捏~
    今日卡运   查看今天打牌运势~
    查卡 ygo卡名 (怪兽|魔法|陷阱) (页码)   查询对应卡牌~
        -例：查卡半龙女仆 怪兽 2
        -注：括号内为选填，如查询到复数结果可以输入1-5选择具体卡牌
            --该功能需要检测查卡后的下一句话，可能会导致下一项指令无效
    价格查询 卡名 (页码)    查询集换社价格
    查询饼图    查询ygo饼图
    抽卡(猜卡)功能 on | off   开/关抽卡功能(仅限管理)
    抽卡(猜卡)cd (数字)   设置抽卡cd(仅限管理)
    查卡方式 1|2|3  切换查卡方式'''
    await ocghelp.send(Message([{
        "type": "image",
        "data": {
            "file": f"base64://{str(image_to_base64(text_to_image(txt)), encoding='utf-8')}"
        }
    }]))

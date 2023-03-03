import io

import numpy
import requests
from PIL import Image, ImageFont, ImageDraw
from matplotlib import pyplot as plt
from matplotlib import font_manager as fm
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Event, Bot, Message
from nonebot import on_command

from src.libraries.image import image_to_base64

url = "https://sapi.moecube.com:444/ygopro/analytics/deck/type?type=day&source=mycard-athletic"

pieChartSearch = on_command("查询饼图")
font_path = "src/static/qmzl.ttf"


@pieChartSearch.handle()
async def test(bot: Bot, event: Event, state: T_State):
    pie_date = requests.get(url).json()
    date_list = list()
    count_list = list()
    elseCount = 0
    fm.fontManager.addfont(font_path)
    prop = fm.FontProperties(fname=font_path)
    print(prop.get_name())
    plt.rcParams['font.family'] = prop.get_name()
    plt.rcParams['font.sans-serif'] = prop.get_name()
    plt.rcParams['axes.unicode_minus'] = False
    for index, item in enumerate(pie_date):
        if index < 6:
            date_list.append(str(item['name']))
            count_list.append(int(item['count']))
        elif index < 12:
            elseCount += int(item['count'])
    date_list.append("其他")
    count_list.append(elseCount)
    colors = plt.get_cmap('Blues')(numpy.linspace(0.9, 0.2, len(date_list)))
    fig = plt.figure("pie", frameon=False)
    canvas = fig.canvas
    plt.title("ygo饼图", fontsize=33,x=0.42,y=1.05)
    patches, l_text, p_text = plt.pie(count_list, labels=date_list, colors=colors, autopct='%1.1f%%')

    for t in l_text:
        t.set_size(17)
    for t in p_text:
        t.set_size(17)

    plt.axis('off')

    fig.set_size_inches(512 / 93, 512 / 93)

    plt.gca().xaxis.set_major_locator(plt.NullLocator())  # plt.gca()表示获取当前子图"Get Current Axes"。

    plt.gca().yaxis.set_major_locator(plt.NullLocator())

    plt.margins(0, 0)

    buffer = io.BytesIO()  # 获取输入输出流对象

    canvas.print_png(buffer)  # 将画布上的内容打印到输入输出流对象

    data = buffer.getvalue()  # 获取流的值

    buffer.write(data)  # 将数据写入buffer

    img = Image.open(buffer)  # 使用Image打开图片数据

    img_back = Image.open("src/static/pie_back.png")

    height, width = img.size

    height2, width2 = img_back.size

    loca = (int((height2 - height) / 2), int((width2 - width) / 2))

    img_back.paste(img, loca, mask=img)

    # =========备注添加
    source = ImageFont.truetype(font_path, 15)
    timefont = ImageFont.truetype(font_path, 25)
    time_up = pie_date[0]['recent_time']
    draw = ImageDraw.Draw(img_back)

    draw.text((int(height2 * 0.7), int(width2 * 0.05)), "数据来源:萌卡数据库", fill=(0, 0, 0), font=source)
    draw.text((int(height2 * 0.1), int(width2 * 0.9)), '更新时间：'+time_up.split("T")[0], fill=(0, 0, 0), font=timefont)
    # =========发送
    await pieChartSearch.finish(Message([{
        "type": "image",
        "data": {
            "file": f"base64://{str(image_to_base64(img_back), encoding='utf-8')}"
        }
    }]))

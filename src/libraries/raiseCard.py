from PIL import ImageFont, ImageDraw, Image

cardpath="src/static/card.jpg"
card2path="src/static/card2.jpg"
fontpath = "src/static/msyh.ttc"

def draw_card_text(text,p):
    if(p==2):
        i = Image.open(card2path)
    else:
        i = Image.open(cardpath)
    draw = ImageDraw.Draw(i)
    width, height = i.size
    if len(text)==1:
        useWid, useHei = width * 0.35, height * 0.08
        size = 120
    elif len(text)==2:
        useWid, useHei = width * 0.3, height * 0.1
        size = 100
    elif len(text) == 3:
        useWid, useHei = width * 0.28, height * 0.11
        size = 70
    else:
        text = text[0:4]
        useWid, useHei = width * 0.26, height * 0.12
        size=60
    font = ImageFont.truetype(fontpath, size)

    draw.text((useWid,useHei), text, font=font, fill=(0, 0, 0))
    return i
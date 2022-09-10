from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import json
from ctypes import windll

a = 0
BM = 0
path = "E:\\wallpaper\\setting.json"


def delta(yy, mm, dd, hh, m):
    global hour, minute, second
    ScheduledTime = datetime(yy, mm, dd, hh, m, 0)           # 设置预定时间
    now = datetime.today()                                   # 获取现在的时间
    Difference = ScheduledTime - now                         # 存储两个时间的时间，差精确到毫秒
    day = Difference.days                                    # 距离预定时间还有多少天
    sec = Difference.seconds                                 # 距离预定时间还有多少秒
    hour = int(sec / 60 / 60)                                # 距离预定时间还有多少小时，并换算为int型
    minute = int(sec / 60 % 60)                              # 距离预定时间还有多少分钟，并换算为int型
    second = sec % 60                                       # 距离预定时间还有多少秒，并换算为int型
    return str(day)


def make_pic(mode, text):
    with open((path), encoding='utf-8') as st:
        backMode = json.load(st)
    img = Image.open(mode["sourse_pic"])
    px = img.size[0]*backMode["text_x"]
    py = img.size[1]*backMode["text_y"]
    sz = int(img.size[0]*backMode["text_size"])
    myfont = ImageFont.truetype(backMode["font"], size=sz)
    draw = ImageDraw.Draw(img)
    tend = len(text)
    draw.text((px, py), text[:tend], font=myfont, fill=backMode["text_color"])
    img.save(mode["output_pic"], quality=100)


def set_wallpaper(img_path):
    windll.user32.SystemParametersInfoW(20, 0, img_path, 0)


def main():
    try:
        with open((path), encoding='utf-8') as st:
            backMode = json.load(st)
        backMode["text"] = backMode["textf"] + str(delta(backMode["yy"], backMode["mm"], backMode["dd"], backMode["hh"], backMode["m"]))+backMode["textl"]
        make_pic(backMode, backMode["text"])
        set_wallpaper(backMode["output_pic"])
        exit(0)           #返回0代表没出错
    except OSError:
        set_wallpaper(backMode["sourse_pic"])
        exit(1)                        #返回1代表OSError
    except KeyboardInterrupt:                      #方便测试，可以省略
        set_wallpaper(backMode["sourse_pic"])
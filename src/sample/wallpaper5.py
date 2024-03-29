from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import json
from ctypes import windll
from time import sleep
a = 0
BM = 0
path = "E:\\wallpaper\\setting.json"


def delta(yy, mm, dd, hh, m):
    ScheduledTime = datetime(yy, mm, dd, hh, m, 0)           # 设置预定时间
    now = datetime.today()                                   # 获取现在的时间
    Difference = ScheduledTime - now                         # 存储两个时间的时间，差精确到毫秒
    day = Difference.days                                    # 距离预定时间还有多少天
    sec = Difference.seconds                                 # 距离预定时间还有多少秒
    hour = int(sec / 60 / 60)                                # 距离预定时间还有多少小时，并换算为int型
    minute = int(sec / 60 % 60)                              # 距离预定时间还有多少分钟，并换算为int型
    #second = sec % 60                                       # 距离预定时间还有多少秒，并换算为int型
    return str(day) + '天 ' + str(hour) + '小时 ' + str(minute) + '分 '


def write_line(backimg, text):  # 给单个文本框填充数据
    px = backimg.size[0]*backMode["text_x"]
    py = backimg.size[1]*backMode["text_y"]
    sz = int(backimg.size[0]*backMode["text_size"])
    myfont = ImageFont.truetype(backMode["font"], size=sz)
    draw = ImageDraw.Draw(backimg)
    tend = len(text)
    draw.text((px, py), text[:tend], font=myfont, fill=backMode["text_color"])
    return backimg


def write_text(img, text):
    tlist = text.split("\n")
    mnum = 0
    for t in tlist:
        tbegin = 0
        tend = len(t)
        while True:
            img, tend = write_line(img, t[tbegin:tend])
            mnum += 1
            if tbegin + tend == len(t):
                break
            else:
                tbegin = tbegin + tend
                tend = len(t)
    return img


def make_pic(mode, text):
    img = Image.open(mode["sourse_pic"])
    img = write_line(img, text)
    img.save(mode["output_pic"], quality=100)


def set_wallpaper(img_path):
    windll.user32.SystemParametersInfoW(20, 0, img_path, 0)


if __name__ == '__main__':
    while True:
        
        with open((path), encoding='utf-8') as st:
            backMode = json.load(st)
        try:
            backMode["text"] = backMode["textf"] + str(delta(backMode["yy"], backMode["mm"], backMode["dd"], backMode["hh"], backMode["m"]))+backMode["textl"]
            make_pic(backMode, backMode["text"])
            set_wallpaper(backMode["output_pic"])
            sleep(58)#这个sleep不能删除，否则无法顺利保存图片，导致OSError
        except OSError:
            set_wallpaper(backMode["sourse_pic"])
        except KeyboardInterrupt:#方便测试，可以省略
            set_wallpaper(backMode["sourse_pic"])
            exit()

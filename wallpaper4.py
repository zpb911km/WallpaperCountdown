from PIL import Image, ImageDraw, ImageFont
from datetime import datetime as dt
import json
import os
import win32gui
import win32con
import win32api
from time import sleep
a = 0
BM = 0


def delta(yy, mm, dd):
    return str((dt(yy, mm, dd)-dt.now()).days)


path = os.path.dirname(__file__)


with open(os.path.join(path, 'setting.json'), encoding='utf-8') as st:
    backMode = json.load(st)
backMode["text"] = backMode["textf"] + \
    str(delta(backMode["yy"], backMode["mm"],
        backMode["dd"]))+backMode["textl"]


def write_line(backimg, text):  # 给单个文本框填充数据
    px = backimg.size[0]*backMode["text_x"]
    py = backimg.size[1]*backMode["text_y"]
    sz = int(backimg.size[0]*backMode["text_size"])
    myfont = ImageFont.truetype(backMode["font"], size=sz)
    draw = ImageDraw.Draw(backimg)
    tend = len(text)
    draw.text((px, py), text[:tend], font=myfont)
    return backimg, tend


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
    img = write_text(img, text)
    img.save(mode["output_pic"], quality=100)


def set_wallpaper(img_path):
    # 打开指定注册表路径
    reg_key = win32api.RegOpenKeyEx(
        win32con.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
    # 最后的参数:2拉伸,0居中,6适应,10填充,0平铺
    win32api.RegSetValueEx(reg_key, "WallpaperStyle", 0, win32con.REG_SZ, "10")
    # 最后的参数:1表示平铺,拉伸居中等都是0
    win32api.RegSetValueEx(reg_key, "TileWallpaper", 0, win32con.REG_SZ, "0")
    # 刷新桌面与设置壁纸
    win32gui.SystemParametersInfo(
        win32con.SPI_SETDESKWALLPAPER, img_path, win32con.SPIF_SENDWININICHANGE)


if __name__ == '__main__':
    while True:
        while True:
            with open(os.path.join(path, 'setting.json'), encoding='utf-8') as st:
                backMode = json.load(st)
            if a != delta(backMode["yy"], backMode["mm"], backMode["dd"]) or BM != backMode["update"]:
                break
            sleep(120)
        a = delta(backMode["yy"], backMode["mm"], backMode["dd"])
        BM = backMode["update"]
        try:
            backMode["text"] = backMode["textf"] + \
                str(delta(backMode["yy"], backMode["mm"],
                    backMode["dd"]))+backMode["textl"]
            make_pic(backMode, backMode["text"])
            set_wallpaper(backMode["output_pic"])
        except OSError:
            set_wallpaper(backMode["sourse_pic"])

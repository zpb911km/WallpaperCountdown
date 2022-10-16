import os.path
import random
from ctypes import windll
from datetime import datetime, timedelta
from time import sleep

from PIL import Image, ImageDraw, ImageFont


PATH_PREFIX: str = os.path.split(__file__)[0]
CONFIGURATION: dict = {
    'time': datetime(datetime.today().year, 6, 7, 9),
    'font': r'C:/Windows/Fonts/STXINWEI.TTF',
    'image': {
        'origin_path': os.path.join(PATH_PREFIX, 'origin.jpg'),
        'output_path': os.path.join(PATH_PREFIX, 'output.jpg'),
    },
    'text': {
        'content': '距离高考还有：%d天%d小时%d分钟',
        'x_position': 0.5,
        'y_position': 0.7,
        'size': 0.05,
        'color': '#f0eef5'
    },
    'glurge': {
        'path': os.path.join(PATH_PREFIX, 'glurge.txt'),
        'size': 0.03,
        'offset': 0.08,
        'color': '#f0eef5'
    }
}


def calc_deltatime() -> tuple[int, int, int]:
    if (now := datetime.today()) >= CONFIGURATION['time']:
        CONFIGURATION['time']: datetime = datetime(
            CONFIGURATION['time'].year + 1,
            CONFIGURATION['time'].month,
            CONFIGURATION['time'].day,
            CONFIGURATION['time'].hour
        )

    delta: timedelta = CONFIGURATION['time'] - now

    return (delta.days, delta.seconds // 3600, delta.seconds // 60 % 60)


def draw_image(text: str, *, with_glurge: bool = True):
    with Image.open(CONFIGURATION['image']['origin_path']) as img:
        ImageDraw.Draw(img).text(
            # 参数一：文字坐标
            xy=(img.size[0] * CONFIGURATION['text']['x_position'],
                img.size[1] * CONFIGURATION['text']['y_position']),
            # 参数二：文本内容
            text=text,
            # 参数三：字体
            font=ImageFont.truetype(CONFIGURATION['font'], size=int(img.size[0] * CONFIGURATION['text']['size'])),
            # 参数四：文字锚点
            anchor='mm',
            # 参数五：文字颜色（RGB值）
            fill=CONFIGURATION['text']['color']
        )

        if with_glurge:
            try:
                with open(CONFIGURATION['glurge']['path'], encoding='UTF-8') as file:
                    ImageDraw.Draw(img).text(
                        xy=(img.size[0] * CONFIGURATION['text']['x_position'],
                            img.size[1] * (CONFIGURATION['text']['y_position'] + CONFIGURATION['glurge']['offset'])),
                        text=random.choice(file.readlines()),
                        font=ImageFont.truetype(CONFIGURATION['font'], size=int(img.size[0] * CONFIGURATION['glurge']['size'])),
                        anchor='mm',
                        fill=CONFIGURATION['text']['color']
                    )
            except FileNotFoundError:
                pass

        # 保存图片
        img.save(CONFIGURATION['image']['output_path'], quality=95)
        # The image quality, on a scale from 0 (worst) to 95 (best), or the string keep.
        # The default is 75. Values above 95 should be avoided;
        # 100 disables portions of the JPEG compression algorithm,
        # and results in large files with hardly any gain in image quality.
        # The value keep is only valid for JPEG files
        # and will retain the original image quality level, subsampling, and qtables.


def set_wallpaper(img_path):
    windll.user32.SystemParametersInfoW(20, 0, img_path, 0)


if __name__ == '__main__':
    while True:
        try:
            draw_image(CONFIGURATION['text']['content'] % calc_deltatime(), with_glurge=True)
            set_wallpaper(CONFIGURATION['image']['output_path'])
            sleep(23)  # 这个sleep不能删除，否则无法顺利保存图片，导致OSError
        except OSError:
            set_wallpaper(CONFIGURATION['image']['origin_path'])
        except KeyboardInterrupt:  # 方便测试，可以省略
            set_wallpaper(CONFIGURATION['image']['origin_path'])
            exit()

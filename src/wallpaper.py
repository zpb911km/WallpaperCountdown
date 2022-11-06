import asyncio
import os.path
import random
import time
from ctypes import POINTER, cast, windll
from datetime import datetime, timedelta

from comtypes import CLSCTX_ALL
from PIL import Image, ImageDraw, ImageFont
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

PATH_PREFIX: str = os.path.split(__file__)[0]
CONFIGURATION: dict = {
    'time': datetime(datetime.today().year, 6, 7, 9),
    'font': r'E:/wallpaper/Fonts/STXINWEI.TTF',
    'image': {
        'origin_path': os.path.join(PATH_PREFIX, 'origin.jpg'),
        'output_path': os.path.join(PATH_PREFIX, 'output.jpg'),  # TODO:增加相对路径的调用
    },
    'text': {
        'content': '距离高考还有：%d天%d小时%d分钟',
        'x_position': 0.5,
        'y_position': 0.75,
        'size': 0.05,
        'color': '#f0eef5'
    },
    'glurge': {
        'path': os.path.join(PATH_PREFIX, 'glurge.txt'),
        'size': 0.03,
        'offset': 0.1,
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
                    # 检查公告
                    content: list[str] = file.readlines()
                    if content[0].startswith('@'):
                        text = content[0][1:]
                    else:
                        text = random.choice(content)

                    ImageDraw.Draw(img).text(
                        xy=(img.size[0] * CONFIGURATION['text']['x_position'],
                            img.size[1] * (CONFIGURATION['text']['y_position'] + CONFIGURATION['glurge']['offset'])),
                        text=text,
                        font=ImageFont.truetype(CONFIGURATION['font'], size=int(img.size[0] * CONFIGURATION['glurge']['size'])),
                        anchor='mm',
                        fill=CONFIGURATION['text']['color']
                    )

            except FileNotFoundError:
                pass

        # 保存图片
        img.save(CONFIGURATION['image']['output_path'], quality=100)
        # The image quality, on a scale from 0 (worst) to 95 (best), or the string keep.
        # The default is 75. Values above 95 should be avoided;
        # 100 disables portions of the JPEG compression algorithm,
        # and results in large files with hardly any gain in image quality.
        # The value keep is only valid for JPEG files
        # and will retain the original image quality level, subsampling, and qtables.


async def set_wallpaper() -> None:
    while True:
        start_time: float = time.monotonic()
        draw_image(CONFIGURATION['text']['content'] % calc_deltatime(), with_glurge=True)
        set_wallpaper(CONFIGURATION['image']['output_path'])
        windll.user32.SystemParametersInfoW(0x14, 0, CONFIGURATION['image']['origin_path'], 0)

        await asyncio.sleep(60 - (time.monotonic() - start_time))


async def adjust_volume() -> None:
    global x_count

    while True:
        now: datetime = datetime.now()
        # 新闻联播：每30s检查一次
        if now.hour == 12 and 20 <= now.minute <= 50:
            v_device = cast(AudioUtilities.GetSpeakers().Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None),
                            POINTER(IAudioEndpointVolume))
            if v_device.GetMasterVolumeLevelScalar() != 0.6:
                x_count += 1
            v_device.SetMasterVolumeLevelScalar(0.6, None)
            await asyncio.sleep(30)
        # 下午：每0~10s检查一次
        elif (now.hour >= 17 and now.minute >= 15) and (now.hour <= 18 and now.minute < 10):
            v_device = cast(AudioUtilities.GetSpeakers().Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None),
                            POINTER(IAudioEndpointVolume))
            if v_device.GetMasterVolumeLevelScalar() != 0.0:
                x_count += 1
            v_device.SetMasterVolumeLevelScalar(0.0, None)
            await asyncio.sleep(random.random() * 10)
        # 晚自习：设置音量为60
        elif now.hour == 18 and now.minute == 10:
            cast(AudioUtilities.GetSpeakers().Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None),
                 POINTER(IAudioEndpointVolume))\
                    .SetMasterVolumeLevelScalar(0.6, None)
            await asyncio.sleep(60)
        else:
            await asyncio.sleep(60)


async def take_extra_action() -> None:
    global x_count

    while True:
        if x_count:
            ...

        await asyncio.sleep(1)


if __name__ == '__main__':
    x_count: int = 0

    loop = asyncio.get_event_loop()
    loop.create_task(set_wallpaper())
    loop.create_task(adjust_volume())
    loop.create_task(take_extra_action())

    time.sleep(60 - datetime.now().second)
    loop.run_forever()

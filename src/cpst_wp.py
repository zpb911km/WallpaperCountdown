import json
import os.path
from datetime import datetime
from typing import TYPE_CHECKING

from PIL import Image, ImageDraw, ImageFont

if TYPE_CHECKING:
    # 不是很有意义但可以让自动补全很爽的Type Hint
    from datetime import timedelta
    from typing import TypedDict

    class DateTimeContainer(TypedDict):
        year: int
        month: int
        day: int
        hour: int
        minute: int
        second: int
        microsecond: int

    class PicturePath(TypedDict):
        rel_folder_path: str
        original_file: str

    class TextPosition(TypedDict):
        x: float
        y: float

    class Text(TypedDict):
        template: str
        position: TextPosition
        size: float
        color: str

    class Config(TypedDict):
        event: str
        scheduled_time: str | DateTimeContainer
        pic: PicturePath
        font_path: str
        text: Text


# 获取当前文件所在文件夹路径
PATH_PREFIX: str = os.path.split(__file__)[0]


def parse_datetime(dt: 'str | DateTimeContainer') -> 'datetime':
    '''
    对支持的两种时间表示格式进行解析。
    '''
    if isinstance(dt, str):
        return datetime.strptime(dt, r'%Y-%m-%d %H:%M:%S')
    else:
        return datetime(**dt)


def composite(cfg: 'Config', dlt_tm: 'timedelta') -> None:
    '''
    合成并保存图片。
    '''
    with Image.open(os.path.join(PATH_PREFIX, cfg['pic']['rel_folder_path'], cfg['pic']['original_file'])) as img:
        # 词穷，不会给变量命名，于是全部塞到一句里
        ImageDraw.Draw(img).text(
            # 参数一：文字坐标
            xy=(img.size[0] * cfg['text']['position']['x'], img.size[1] * cfg['text']['position']['y']),
            # 参数二：文本内容
            text=cfg['text']['template'] % {'event': cfg['event'], 'day': dlt_tm.days},
            # 参数三：字体
            font=ImageFont.truetype(cfg['font_path'], size=int(img.size[0] * cfg['text']['size'])),
            # 参数四：文字锚点
            anchor='mm',
            # 参数五：文字颜色（RGB值）
            fill=cfg['text']['color']
        )
        # 保存图片
        img.save(os.path.join(PATH_PREFIX, cfg['pic']['rel_folder_path'], 'tmp', 'wallpaper.png'))


if __name__ == '__main__':
    try:
        with open(os.path.join(PATH_PREFIX, r'config.json'), encoding='UTF-8') as json_file:
            config: 'Config' = json.load(json_file)
        scheduled_time: 'datetime' = parse_datetime(config['scheduled_time'])
        composite(config, scheduled_time - datetime.today())
    except Exception:
        # 捕获所有非系统异常，并将信息输出至日志文件。
        import traceback
        with open(os.path.join(PATH_PREFIX, 'log.txt'), 'a', encoding='UTF-8') as file:
            file.write(datetime.strftime(datetime.today(), r'%Y-%m-%d %H:%M:%S'))
            file.write('\n')
            file.write('An unhandled exception occured while the program was running:\n')
            file.write('\n')
            file.write(traceback.format_exc())
            file.write('\n')
            file.write('-' * 20 + '\n')
        exit(1)
    else:
        exit(0)

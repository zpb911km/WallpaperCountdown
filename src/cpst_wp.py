import json
import os.path
from datetime import datetime
from typing import TYPE_CHECKING

from PIL import Image, ImageDraw, ImageFont

if TYPE_CHECKING:
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


PATH_PREFIX: str = os.path.split(__file__)[0]


def parse_datetime(dt: 'str | DateTimeContainer') -> 'datetime':
    if isinstance(dt, str):
        return datetime.strptime(dt, r'%Y-%m-%d %H:%M:%S')
    else:
        return datetime(**dt)


def composite(cfg: 'Config', dlt_tm: 'timedelta') -> None:
    with Image.open(os.path.join(PATH_PREFIX, cfg['pic']['rel_folder_path'], cfg['pic']['original_file'])) as img:
        ImageDraw.Draw(img).text(
            xy=(img.size[0] * cfg['text']['position']['x'], img.size[1] * cfg['text']['position']['y']),
            text=cfg['text']['template'] % {'event': cfg['event'], 'day': dlt_tm.days},
            font=ImageFont.truetype(cfg['font_path'], size=int(img.size[0] * cfg['text']['size'])),
            fill=cfg['text']['color']
        )
        img.save(os.path.join(PATH_PREFIX, cfg['pic']['rel_folder_path'], 'tmp', 'wallpaper.png'))


if __name__ == '__main__':
    try:
        with open(os.path.join(PATH_PREFIX, r'config.json'), encoding='UTF-8') as json_file:
            config: 'Config' = json.load(json_file)
        scheduled_time: 'datetime' = parse_datetime(config['scheduled_time'])
        composite(config, scheduled_time - datetime.today())
    except Exception:
        import traceback
        with open(os.path.join(PATH_PREFIX, 'log.txt'), encoding='UTF-8') as file:
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

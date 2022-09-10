import datetime     # 引入datetime模块
import time         # 引入time模块

AScheduledTime = datetime.datetime(2020, 6, 18, 0, 0, 0)  # 设置预定时间
Anow = datetime.datetime.today()                          # 获取现在的时间
ADifference = AScheduledTime - Anow                       # 存储两个时间的时间，差精确到毫秒
Asec = ADifference.seconds                                # 距离预定时间还有多少秒

while (Asec):
    while (1):
        ScheduledTime = datetime.datetime(2023, 6, 7, 0, 0, 0)  # 设置预定时间
        now = datetime.datetime.today()                          # 获取现在的时间
        Difference = ScheduledTime - now                         # 存储两个时间的时间，差精确到毫秒
        day = Difference.days                                    # 距离预定时间还有多少天
        sec = Difference.seconds                                 # 距离预定时间还有多少秒
        hour = int(sec / 60 / 60)                                # 距离预定时间还有多少小时，并换算为int型
        minute = int(sec / 60 % 60)                              # 距离预定时间还有多少分钟，并换算为int型
        second = sec % 60                                        # 距离预定时间还有多少秒，并换算为int型

        print('距离结束：' + str(day) + '天 ' + str(hour) + '时 ' + str(minute) + '分 ' + str(second) + '秒')

        time.sleep(1)
    Asec -= 1

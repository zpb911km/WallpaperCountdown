from win32process import CreateProcess, CREATE_NO_WINDOW, STARTUPINFO
from win32gui import FindWindow
from win32api import GetSystemMetrics
from win32con import SM_CXSCREEN, SM_CYSCREEN
from time import sleep
from win32gui import FindWindow, FindWindowEx, ShowWindow, SendMessageTimeout, SetParent, EnumWindows, GetWindowText
from win32con import SW_HIDE, SMTO_ABORTIFHUNG, SW_SHOW


def _MyCallback(hwnd, extra):#遍历窗口函数的回调函数（提前return退出遍历会报错）
    #当前窗口中查找图标窗口
    icon_window = FindWindowEx(hwnd, None, "SHELLDLL_DefView", None)
    if(icon_window):#当前窗口包含图标窗口
        #查找静态壁纸窗口并保存
        extra[0] = FindWindowEx(None, hwnd, "WorkerW", None)


def RunVideoWallpaper(player_window_handel):#设置视频壁纸
    if(player_window_handel):
        #查找桌面窗口
        desktop_window_handel = FindWindow("Progman", "Program Manager")
        #设置player_window为desktop_window的子窗口
        SetParent(player_window_handel, desktop_window_handel)
        #核心语句，向desktop_window发送0x52C启用Active Desktop
        SendMessageTimeout(desktop_window_handel, 0x52C, 0, 0, SMTO_ABORTIFHUNG, 1000)
        #因为有两个同类同名的WorkerW窗口，所以遍历所有顶层窗口
        workerw=[0]
        EnumWindows(_MyCallback, workerw)
        #获取player_windows名称
        player_windows_name = GetWindowText(player_window_handel)
        while(True):#防止win+tab导致静态壁纸窗口重新出现及将player_window发送到图标窗口的父窗口(原因不明)
            #隐藏静态壁纸窗口
            ShowWindow(workerw[0], SW_HIDE)
            #判断player_window是否在desktop_window下
            player_under_desktop = FindWindowEx(desktop_window_handel, None, "SDL_app", player_windows_name)
            if(player_under_desktop==0):#如果player_window位置不正确
                #将player_window设置为desktop_window的子窗口
                SetParent(player_window_handel, desktop_window_handel)

if __name__ == "__main__":
   #获得屏幕分辨率
    screen_width = GetSystemMetrics(SM_CXSCREEN)
    screen_screen = GetSystemMetrics(SM_CYSCREEN)
    #视频地址
    video_path = r"D:\新建文件夹 (2)\CatCatch\g3148lls29f.mp4"
    #自定义播放设置：不显示字幕，静音
    custom_settings = '-sn -noborder'
    #自定义播放设置：初始音量10
    #custom_settings ='-volume 10'
    #默认播放设置：全屏，强制分辨率，无限循环，无输出
    cmdline = "-fs -top 550 -left 1050 -x 400 -loop 0 \"{0}\" -loglevel quiet ".format(video_path) + custom_settings
    #播放器地址
    ffplay_path=r"E:\ffmpeg\bin\ffplay.exe"
    #创建播放器进程(无窗口)
    CreateProcess(ffplay_path, cmdline, None, None, 0, CREATE_NO_WINDOW, None, None, STARTUPINFO())
    while(True):#等待播放器窗口创建完毕
        #查找播放器窗口
        player_window_handel = FindWindow("SDL_app", video_path)
        if(player_window_handel!=0):#找到播放器窗口
            #视频窗口窗口原点会不在00，sleep可以解决
            sleep(0.1)
            break
    #开始视频壁纸
    RunVideoWallpaper(player_window_handel)
from Util import TimeMeasuring
from ImgTools import Recognize
import os
from PIL import Image


def GetScreenshot():
    os.system('adb exec-out screencap -p > screenshot.png')
    scr = Image.open('screenshot.png')
    scr = scr.crop([0, 700, 1080, 1200])
    return scr


@TimeMeasuring
def Play():
    flag = ""
    while True:
        scr = GetScreenshot()
        expr = Recognize(scr)
        print(expr, eval(expr))
        if flag == expr:
            continue
        else:
            flag = expr
            if eval(expr):
                os.system("adb shell input tap 300 1500")
            else:
                os.system("adb shell input tap 800 1500")


if __name__ == '__main__':
    Play()

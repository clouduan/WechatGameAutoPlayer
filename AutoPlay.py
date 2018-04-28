from Util import Time_using
from ImgTools import Recognize
import os


@Time_using
def Play():
    flag = ""
    while True:
        os.system('adb exec-out screencap -p > screenshot.png')
        expr = Recognize('screenshot.png')
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

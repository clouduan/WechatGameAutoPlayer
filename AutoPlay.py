from Recognize import Recognize
import os
import subprocess
import sys
import time


def GetScreenshot(picName='screenshot.png'):
    # os.system("adb devices")
    process = subprocess.Popen('adb shell screencap -p', shell=True, stdout=subprocess.PIPE)
    screenshot = process.stdout.read()
    # print(screenshot)
    if sys.platform == 'win32':
        screenshot = screenshot.replace(b'\r\n', b'\n')

    with open(picName, 'wb') as f:
        f.write(screenshot)


def Judge(image):
    ocr = Recognize()
    expr = ocr.Recognize(image)
    print(expr, eval(expr))
    return eval(expr)


def Click():
    if Judge('./screenshot.png') == True:
        os.system("adb shell input tap 300 1500")
    else:
        os.system("adb shell input tap 800 1500")


def Play():
    i = 0
    while True:
        GetScreenshot()
        # time.sleep(0.1)
        Click()
        i += 1
        time.sleep(0.1)


if __name__ == '__main__':
    Play()

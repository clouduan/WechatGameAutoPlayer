from Recognize import Recognize
import os
import subprocess
import sys
import time
from io import BytesIO


def GetScreenshot(picName='screenshot.png'):
    process = subprocess.Popen('adb shell screencap -p', shell=True, stdout=subprocess.PIPE)
    screenshot = process.stdout.read()
    if screenshot == b'':
        print('Please make sure you can run adb commands successfully.')
        os._exit(0)

    if sys.platform == 'win32':
        screenshot = screenshot.replace(b'\r\n', b'\n')

    if picName:
        with open(picName, 'wb') as f:
            f.write(screenshot)
    # 直接在内存中读写，节约时间
    imgFile = BytesIO(screenshot)
    return imgFile


def Judge(image):
    ocr = Recognize()
    expr = ocr.Recognize(image)
    print(expr, eval(expr))
    return eval(expr)


def Click(judgement):
    if judgement == True:
        os.system("adb shell input tap 300 1500")
    else:
        os.system("adb shell input tap 800 1500")


def Play():
    while True:
        screenshot = GetScreenshot()
        judgement = Judge(screenshot)
        Click(judgement)


if __name__ == '__main__':
    Play()

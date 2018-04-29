import time


def TimeMeasuring(func):
    def wrap(*args, **kwargs):
        time_flag = time.perf_counter()
        result = func(*args)
        print(func.__name__ + ': %.5fs' % (time.perf_counter() - time_flag))
        return result

    return wrap


from io import BytesIO
from ImgTools import *
from pymouse import PyMouse
from PIL import Image
import pyscreenshot as ImageGrab
import subprocess
import os
import json


@TimeMeasuring
def recognize(img):
    img = Binaryzation(img)

    horizontalSegImgs = HorizontalCut(img)
    characterList1 = VerticalCut(horizontalSegImgs[0])
    characterList2 = VerticalCut(horizontalSegImgs[1])

    with open('HashFiles/hash.json', 'r') as fp:
        hashValsDict = json.load(fp)

    # 相近度列表
    nearness1 = {}
    expr = ''
    for characterImg in characterList1:
        hashVal = Hash(characterImg)
        for c in hashValsDict:
            nearness1[c] = HammingDistance(hashVal, hashValsDict[c])
        expr += sorted(nearness1.items(), key=lambda d: d[1])[0][0]

    nearness2 = {}
    for characterImg in characterList2:
        hashVal = Hash(characterImg)
        for c in hashValsDict:
            nearness2[c] = HammingDistance(hashVal, hashValsDict[c])
        expr += sorted(nearness2.items(), key=lambda d: d[1])[0][0]

    expr = expr.replace('subtract', '-')
    expr = expr.replace('plus', '+')
    expr = expr.replace('equal', '==')

    return expr


@TimeMeasuring
def get_screenshot_adb_1():
    process = subprocess.Popen('adb shell screencap -p', shell=True, stdout=subprocess.PIPE)
    screenshot = process.stdout.read()
    imgFile = BytesIO(screenshot)
    img = Image.open(imgFile)


@TimeMeasuring
def get_screenshot_adb_2():
    os.system('adb exec-out screencap -p > screenshot.png')
    img = Image.open('screenshot.png')


@TimeMeasuring
def simulate_click_adb():
    os.system('adb shell input tap 300 1500')


@TimeMeasuring
def get_screenshot_linux_1():
    '''
    不支持预选定area
    '''
    im = ImageGrab.grab()


@TimeMeasuring
def get_screenshot_linux_2():
    os.system('import -window root -crop 300x180+100+300 screenshot.png')
    src = Image.open('screenshot.png')
    return src


@TimeMeasuring
def get_screenshot_linux_3():
    '''
    不支持预选定area
        '''
    os.system('scrot screenshot.png')


@TimeMeasuring
def get_screenshot_linux_4():
    '''
    不支持预选定area
    '''
    os.system('gnome-screenshot -f screenshot.png')


@TimeMeasuring
def simulate_click_pc():
    m = PyMouse()
    m.click(150, 650, 1)


@TimeMeasuring
def get_screenshot_windows():
    from PIL import ImageGrab
    img = ImageGrab.grab([100, 100, 400, 400])


if __name__ == '__main__':
    pass

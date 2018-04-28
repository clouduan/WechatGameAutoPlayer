from Util import Time_using
import subprocess
from io import BytesIO
from ImgTools import *
import json
from PIL import Image
import os


@Time_using
def get_screenshot1():
    process = subprocess.Popen('adb shell screencap -p', shell=True, stdout=subprocess.PIPE)
    screenshot = process.stdout.read()
    imgFile = BytesIO(screenshot)
    img = Image.open(imgFile)


@Time_using
def get_screenshot2():
    os.system('adb exec-out screencap -p > screenshot.png')
    img = Image.open('screenshot.png')


@Time_using
def click():
    os.system('adb shell input tap 300 1500')


@Time_using
def recognize(imgFile):
    img = Image.open(imgFile).convert('L')
    img = img.crop([0, 700, 1080, 1200])
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


if __name__ == '__main__':
    get_screenshot1()
    get_screenshot2()
    click()
    recognize('Screenshots/0th.png')

    pass

from PIL import Image
from Util import Time_using
import numpy as np
import json


def Binaryzation(img, threshold=220):
    img = img.convert('L')
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    binImg = img.point(table, '1')
    return binImg


@Time_using
def VerticalCut(binImg):
    _, height = binImg.size
    # 列表保存像素累加值大于0的列
    x0 = []
    pix = np.array(binImg)
    xp = list(np.sum(pix, axis=0))
    for x in range(len(xp)):
        if xp[x] > 10:
            x0.append(x)
    # 找出边界
    segList = []
    segList.append(x0[0])
    for i in range(1, len(x0)):
        if abs(x0[i] - x0[i - 1]) > 1:
            segList.extend([x0[i - 1], x0[i]])
    segList.append(x0[-1])

    imgList = []
    # 判断是整对
    if len(segList) % 2 == 0:
        for i in range(len(segList) // 2):
            segImg = binImg.crop([segList[i * 2], 0, segList[i * 2 + 1], height])
            imgList.append(segImg)
        return imgList
    else:
        return False


@Time_using
def HorizontalCut(binImg):
    width, _ = binImg.size
    y0 = []
    pix = np.array(binImg)
    yp = list(np.sum(pix, axis=1))
    for y in range(len(yp)):
        if yp[y] > 10:
            y0.append(y)
    # 找出边界
    segList = []
    segList.append(y0[0])
    for i in range(1, len(y0)):
        if abs(y0[i] - y0[i - 1]) > 1:
            segList.extend([y0[i - 1], y0[i]])
    segList.append(y0[-1])

    if len(segList) == 4:
        segImg1 = binImg.crop([0, segList[0], width, segList[1]])
        segImg2 = binImg.crop([0, segList[2], width, segList[3]])
        return [segImg1, segImg2]
    else:
        return False


def Hash(img):
    img = img.resize((10, 15), Image.LANCZOS).convert("L")
    pixels = np.array(img).flatten()
    avg = pixels.mean()
    hashVal = ''
    for i in pixels:
        if i > avg:
            hashVal += '1'
        else:
            hashVal += '0'
    return hashVal


def HammingDistance(hash1, hash2):
    if len(hash1) != len(hash2):
        print(hash1, hash2)
        raise ValueError("Undefined for sequences of unequal length")
    return sum(i != j for i, j in zip(hash1, hash2))


@Time_using
def Recognize(imgFile):
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
    """
    以下代码只用于debug
    """
    expr = Recognize('./Screenshots/0th.png')

    print(expr)

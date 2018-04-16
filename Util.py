from Preprocess import Preprocess
from Recognize import Recognize
from AutoPlay import GetScreenshot
from PIL import Image
import os
import time
import json


def GetScreenshots():
    for i in range(50):
        GetScreenshot('Screenshots/' + str(i))
        time.sleep(1)


def GetCharacters():
    pp = Preprocess()
    for imgName in os.listdir('./Screenshots/'):
        img = Image.open('./Screenshots/' + imgName)
        img = pp.Binaryzation(img.crop([0, 700, 1080, 1200]))
        horizontalSegImgs = pp.HorizontalSegmentation(img)
        vertialSegImgs = pp.VerticalSegmentation(horizontalSegImgs[1])
        # vertialSegImgs = pp.VerticalSegmentation(horizontalSegImgs[1])
        for character in vertialSegImgs:
            character.show()
            picName = input('name:')
            if picName != '':
                character.save('./Characters/' + picName + '.png')


def GetHashValue():
    ocr = Recognize()
    hashValsDict = {}
    for character in os.listdir('./Characters/'):
        img = Image.open('./Characters/' + character)
        hashVal = ocr.Hash(ocr.Binaryzation(img))
        characterName = character[:-4]
        hashValsDict[characterName] = hashVal

    with open('HashFiles/hash.json', 'w') as fp:
        json.dump(hashValsDict, fp)


# GetCharacters()
GetHashValue()

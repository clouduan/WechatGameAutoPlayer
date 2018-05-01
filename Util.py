from ImgTools import *
from PIL import Image
import os
import time
import json


def GetScreenshots():
    for i in range(50):
        os.system('adb exec-out screencap -p > {0}th.png'.format(i))
        time.sleep(1)


def GetCharacters():
    for imgName in os.listdir('Screenshots'):
        img = Image.open(os.path.join('Screenshots', imgName))
        img = Binaryzation(img.crop([0, 700, 1080, 1200]))
        horizontalSegImgs = HorizontalCut(img)
        vertialSegImgs = VerticalCut(horizontalSegImgs[1])
        # vertialSegImgs = VerticalCut(horizontalSegImgs[1])
        for character in vertialSegImgs:
            character.show()
            picName = input('name:')
            if picName != '':
                character.save('Characters/{0}.png'.format(picName))


def GetHashValue():
    hashValsDict = {}
    for character in os.listdir('Characters'):
        img = Image.open(os.path.join('Characters', character))
        hashVal = Hash(Binaryzation(img))
        characterName = character[:-4]
        hashValsDict[characterName] = hashVal

    with open('HashFiles/hash.json', 'w') as fp:
        json.dump(hashValsDict, fp)

    return True


if __name__ == '__main__':
    # GetCharacters()
    GetHashValue()

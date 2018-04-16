from PIL import Image
from Preprocess import Preprocess
import json
import numpy
import time


class Recognize(Preprocess):
    def Recognize(self, screenshot):
        img = Image.open(screenshot).convert('L')
        img = img.crop([0, 700, 1080, 1200])
        img = self.Binaryzation(img)

        horizontalSegImgs = self.HorizontalSegmentation(img)
        characterList1 = self.VerticalSegmentation(horizontalSegImgs[0])
        characterList2 = self.VerticalSegmentation(horizontalSegImgs[1])

        with open('./HashFiles/hash.json', 'r') as fp:
            hashValsDict = json.load(fp)

        # 相近度列表
        nearness1 = {}
        expr = ''
        for characterImg in characterList1:
            hashVal = self.Hash(characterImg)
            for c in hashValsDict:
                nearness1[c] = self.HammingDistance(hashVal, hashValsDict[c])
            expr += sorted(nearness1.items(), key=lambda d: d[1])[0][0]

            nearness2 = {}
        for characterImg in characterList2:
            hashVal = self.Hash(characterImg)
            for c in hashValsDict:
                nearness2[c] = self.HammingDistance(hashVal, hashValsDict[c])
            expr += sorted(nearness2.items(), key=lambda d: d[1])[0][0]

        expr = expr.replace('subtract', '-')
        expr = expr.replace('plus', '+')
        expr = expr.replace('equal', '==')

        return expr

    def HammingDistance(self, hash1, hash2):
        if len(hash1) != len(hash2):
            print(hash1, hash2)
            raise ValueError("Undefined for sequences of unequal length")
        return sum(i != j for i, j in zip(hash1, hash2))

    def Hash(self, img):
        img = img.resize((40, 60), Image.LANCZOS).convert("L")
        pixels = numpy.array(img).flatten()
        avg = pixels.mean()
        hashVal = ''
        for i in pixels:
            if i > avg:
                hashVal += '1'
            else:
                hashVal += '0'
        return hashVal


if __name__ == '__main__':
    """
    以下代码只用于debug
    """
    ocr = Recognize()
    # for i in os.listdir('./Screenshots/'):
    #    expr=ocr.Recognize('./Screenshots/'+i)
    #    print(expr)

    # t1=time.clock()
    expr = ocr.Recognize('./test/13.png')
    # t2=time.clock()
    # print(t2-t1)

    print(expr)

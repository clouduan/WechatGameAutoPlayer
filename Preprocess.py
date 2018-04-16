from PIL import Image


class Preprocess(object):

    def Binaryzation(self, img, threshold=220):
        img = img.convert('L')
        table = []
        for i in range(256):
            if i < threshold:
                table.append(0)
            else:
                table.append(1)
        binImg = img.point(table, '1')
        return binImg

    def VerticalSegmentation(self, binImg):
        width, height = binImg.size
        pix = binImg.load()
        # 列表保存像素累加值大于0的列
        x0 = []
        for x in range(width):
            pixels = sum(pix[x, y] == 1 for y in range(height))
            # 此处设置一个阀值，只有当累积像素大于阀值时才表明图像像素连续
            if pixels > 10:
                x0.append(x)
        # print(x0)
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

    def HorizontalSegmentation(self, binImg):
        width, height = binImg.size
        pix = binImg.load()
        # 列表保存像素累加值大于0的列
        y0 = []
        for y in range(height):
            pixels = sum(pix[x, y] == 1 for x in range(width))
            # 此处设置一个阀值，只有当累积像素大于阀值时才表明图像像素连续
            if pixels > 10:
                y0.append(y)
        # print(y0)
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


if __name__ == '__main__':
    """
    以下代码只用于debug
    """
    pp = Preprocess()
    img = Image.open('./Screenshots/3th.png')
    print(img.size)
    img = pp.Binaryzation(img.crop([0, 700, 1080, 1200]))
    # pp.Binaryzation(img).show()
    # img.show()
    horizontalSegImgs = pp.HorizontalSegmentation(img)
    vertialSegImgs = pp.VerticalSegmentation(horizontalSegImgs[1])
    vertialSegImgs[1].show()

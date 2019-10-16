from PIL import Image
from pymouse import PyMouse
from ImgTools import recognize
from TimeIt import time_it
from Config import location_on_pc as loc
import os
import time
import sys
import traceback
import math
import cv2
import matplotlib.pyplot as plt
    # 'right_buttom_x': 698,
    # 'right_buttom_y': 438,
ctrl_center = (62, 373)
Radius = 40
@time_it
def get_screenshot():
    if sys.platform == 'win32' or sys.platform == 'darwin':
        from PIL import ImageGrab
        scr = ImageGrab.grab(
            [loc['left_top_x'], loc['left_top_y'], loc['right_buttom_x'], loc['right_buttom_y']])
        scr.save('screenshot.png')
        return scr
    elif sys.platform == 'linux':
        command = 'import -window root -crop {0}x{1}+{2}+{3} screenshot.png'
        command = command.format(loc['right_buttom_x'] - loc['left_top_x'],
                                 loc['right_buttom_y'] - loc['left_top_y'],
                                 loc['left_top_x'],
                                 loc['left_top_y'])
        os.system(command)
        scr = Image.open('screenshot.png')
        return scr
    else:
        print('Unsupported platform: ', sys.platform)
        os._exit(0)

def GetClickPos(theta, center, radius) :
    x = center[0] + radius * math.cos(theta * math.pi / 180.0)
    y = center[1] + radius * math.sin(theta * math.pi / 180.0)
    return (x, y)

def Region(img):
    from skimage import data, util
    from skimage.measure import label, regionprops
    kernel = cv2.getStructuringElement(cv2.MORPH_ERODE,(5, 5))
    eroded = cv2.erode(img,kernel)
    #显示腐蚀后的图像
    label_img = label(eroded, connectivity = 2)
    props = regionprops(label_img)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4))
    ax1.imshow(eroded, plt.cm.gray, interpolation='nearest')
    ax1.axis('off')
    ax2.imshow(label_img,interpolation='nearest')
    ax2.axis('off')
    fig.tight_layout()
    plt.show()
    # centroid of first labeled object props[0]['centroid']
    return props

def SortCentroid(c):
    return c.bbox_area

def CalThetah():
    im = cv2.imread("./screenshot.png")
    gray = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)  #把输入图像灰度化
    #直接阈值化是对输入的单通道矩阵逐像素进行阈值分割。
    ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    shape = gray.shape
    radius = 70
    im_crop = gray[int(shape[0] / 2 - radius) : int(shape[0] / 2 + radius), int(shape[1] / 2 - radius) : int(shape[1] / 2) + radius] 
    im_crop_bin = binary[int(shape[0] / 2 - radius) : int(shape[0] / 2 + radius), int(shape[1] / 2 - radius) : int(shape[1] / 2) + radius]

    centers = Region(im_crop_bin)

    valid_centroid = []
    for p in centers:
        if p.bbox_area > 12:
            valid_centroid.append(p)
            # cv2.circle(im_crop, (int(p.centroid[1]), int(p.centroid[0])), 5, (0,255,0), 2)
    valid_centroid = sorted(centers, key=SortCentroid)
    cv2.circle(im_crop, (int(valid_centroid[-1].centroid[1]), int(valid_centroid[-1].centroid[0])), 5, (0,255,0), 2)
    cv2.circle(im_crop, (int(valid_centroid[-2].centroid[1]), int(valid_centroid[-2].centroid[0])), 5, (0,255,0), 2)
    cv2.circle(im_crop, (int(valid_centroid[-3].centroid[1]), int(valid_centroid[-3].centroid[0])), 5, (0,255,0), 2)

    # cv2.namedWindow("liantiong", 1)
    cv2.imshow("laintiong", im_crop)
    cv2.waitKey(0)
    # imgray=cv2.Canny(im_crop, 30, 100)

    # circles = cv2.HoughCircles(imgray,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=10,maxRadius=30)
    # for i in circles[0,:]:
    # # draw the outer circle
    #     cv2.circle(im_crop,(i[0],i[1]),i[2],(0,255,0),2)
    # print("threshold value %s"%ret)
    # cv2.namedWindow("binary0", 1)
    # cv2.imshow("binary0", im_crop)
    # cv2.waitKey(0)

def Play():
    m = PyMouse()
    theta = 0
    cnt = 100
    
    clicked_pos = GetClickPos(theta, ctrl_center, Radius)
    m.click(clicked_pos[0], clicked_pos[1])
    m.press(clicked_pos[0], clicked_pos[1])
    
    while cnt > 0:
        # start = time.perf_counter()
        cnt -= 1
        # time.sleep(0.1)
        try:
            # scr = get_screenshot()
            # expr = recognize(scr)
            theta += 45
            move_pos = GetClickPos(theta, ctrl_center, Radius)
            print(move_pos)
            m.move(move_pos[0], move_pos[1])
            
            time.sleep(0.1)
            print("Once!")
        except:
            print('Error occurred: ')
        # print('One loop: ', time.perf_counter() - a)

    m.release(clicked_pos[0], clicked_pos[1])


if __name__ == '__main__':
    # Play()
    CalThetah()

import os
import sys
import json
import time
import traceback
import numpy as np
from PIL import Image
from pymouse import PyMouse
from util import timing
from config import location_on_pc as loc
from config import threshold


@timing
def get_screenshot():
    if sys.platform == 'win32':
        from PIL import ImageGrab
        scr = ImageGrab.grab([loc['left_top_x'],
                              loc['left_top_y'],
                              loc['right_buttom_x'],
                              loc['right_buttom_y']])
        # scr.save('screenshot.png')
        return scr
    elif sys.platform == 'linux':
        cmd = 'import -window root -crop {0}x{1}+{2}+{3} screenshot.png'
        cmd = cmd.format(loc['right_buttom_x'] - loc['left_top_x'],
                         loc['right_buttom_y'] - loc['left_top_y'],
                         loc['left_top_x'],
                         loc['left_top_y'])
        os.system(cmd)
        scr = Image.open('screenshot.png')
        return scr
    else:
        print('Unsupported platform: ', sys.platform)
        sys.exit()


@timing
def binarize(img, threshold=threshold):
    """二值化"""
    img = img.convert('L')
    table = []
    for i in range(256):
        if i > threshold:
            table.append(0)
        else:
            table.append(1)
    bin_img = img.point(table, '1')
    return bin_img


@timing
def vertical_cut(img):
    """纵向切割"""
    _, height = img.size
    px = list(np.sum(np.array(img) == 0, axis=0))
    # 列表保存像素累加值大于0的列
    x0 = []
    for x in range(len(px)):
        if px[x] > 1:
            x0.append(x)
    
    # 找出边界
    cut_list = [x0[0]]
    for i in range(1, len(x0)):
        if abs(x0[i] - x0[i - 1]) > 1:
            cut_list.extend([x0[i - 1], x0[i]])
    cut_list.append(x0[-1])
    
    cut_imgs = []
    # 切割顺利的话应该是整对
    if len(cut_list) % 2 == 0:
        for i in range(len(cut_list) // 2):
            cut_img = img.crop([cut_list[i * 2], 0, cut_list[i * 2 + 1], height])
            cut_imgs.append(cut_img)
        return cut_imgs
    else:
        print('Vertical cut failed.')
        return


@timing
def horizontal_cut(img):
    """横向切割"""
    width, _ = img.size
    px = list(np.sum(np.array(img) == 0, axis=1))
    # 列表保存像素累加值大于0的行
    y0 = []
    for y in range(len(px)):
        if px[y] > 1:
            y0.append(y)
    
    # 找出边界
    cut_list = [y0[0]]
    for i in range(1, len(y0)):
        if abs(y0[i] - y0[i - 1]) > 1:
            cut_list.extend([y0[i - 1], y0[i]])
    cut_list.append(y0[-1])
    
    # 切割顺利的话应该是长度为4的list
    if len(cut_list) == 4:
        cut_img1 = img.crop([0, cut_list[0], width, cut_list[1]])
        cut_img2 = img.crop([0, cut_list[2], width, cut_list[3]])
        return [cut_img1, cut_img2]
    else:
        print('Horizontal cut failed.')
        return


@timing
def hashing(img):
    """计算哈希值"""
    img = img.resize((20, 30), Image.LANCZOS).convert("L")
    px = np.array(img).flatten()
    hash_val = (px > px.mean()).astype(int)
    hash_val = ''.join(str(e) for e in hash_val)
    return hash_val


@timing
def hamming(hash1, hash2):
    """计算汉明距离"""
    if len(hash1) != len(hash2):
        print('hash1: ', hash1)
        print('hash2: ', hash2)
        raise ValueError("Undefined for sequences of unequal length")
    
    return sum(i != j for i, j in zip(hash1, hash2))


@timing
def recognize(img):
    """输入：经过裁剪的只含有算式的区域图像"""
    img = img.convert('L')
    img = binarize(img)
    
    h_cut_imgs = horizontal_cut(img)
    chars1 = vertical_cut(h_cut_imgs[0])
    chars2 = vertical_cut(h_cut_imgs[1])
    
    with open('HashFiles/hash.json', 'r') as fp:
        hash_vals = json.load(fp)
    
    # 相近度列表
    nearness1 = {}
    expr = ''
    for char in chars1:
        hash_val = hashing(char)
        for h in hash_vals:
            nearness1[h] = hamming(hash_val, hash_vals[h])
        expr += sorted(nearness1.items(), key=lambda d: d[1])[0][0]
    
    nearness2 = {}
    for char in chars2:
        hash_val = hashing(char)
        for h in hash_vals:
            nearness2[h] = hamming(hash_val, hash_vals[h])
        expr += sorted(nearness2.items(), key=lambda d: d[1])[0][0]
    
    expr = expr.replace('subtract', '-').replace('plus', '+').replace('equal', '==')
    
    return expr


def get_hashfile():
    """获得图像的 hash 值保存进 json 文件，用于前期处理"""
    hash_vals = {}
    for char in os.listdir('Characters'):
        img = Image.open(os.path.join('Characters', char))
        hash_val = hashing(binarize(img))
        char_name = char[:-4]
        hash_vals[char_name] = hash_val
    
    with open('HashFiles/hash.json', 'w') as fp:
        json.dump(hash_vals, fp)


def get_chars():
    """从截图样本中得到单个字符的图像，用于前期处理"""
    for img_name in os.listdir('Screenshots'):
        img = Image.open(os.path.join('Screenshots', img_name))
        img = binarize(img.crop([0, 700, 1080, 1200]))
        h_cut_imgs = horizontal_cut(img)
        char_list1 = vertical_cut(h_cut_imgs[0])
        # char_list2 = vertical_cut(h_cut_imgs[1])
        for char in char_list1:
            char.show()
            pic_name = input('name:')
            if pic_name != '':
                char.save('Characters/{0}.png'.format(pic_name))


def Play():
    m = PyMouse()
    flag = ""
    while True:
        # start = time.perf_counter()
        time.sleep(0.1)
        try:
            scr = get_screenshot()
            expr = recognize(scr)
            # 防止重复点击
            if flag == expr:
                continue
            else:
                print("%-15s %-5s" % (expr, eval(expr)))
                flag = expr
                if eval(expr):
                    m.click(loc['click_true_x'], loc['click_true_y'], 1)
                else:
                    m.click(loc['click_false_x'], loc['click_false_y'], 1)
        except:
            if 'scr' in vars():
                scr.save('failed.png')
            print('Error occurred: ')
            print(traceback.print_exc())
            sys.exit()
        # print('One loop: ', time.perf_counter() - a)


if __name__ == '__main__':
    Play()

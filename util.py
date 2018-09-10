"""
生成预 hash 文件；检查 config 中 location_on_pc 是否配置好
"""
import sys
import os
import json
from imgtools import *
from config import location_on_pc as loc


def get_hashfile():
    """获得图像的 hash 值保存进 json 文件，用于前期处理"""
    hash_vals = {}
    for char in os.listdir('Characters'):
        img = Image.open(os.path.join('Characters', char))
        hash_val = hashing(binarize(img))
        char_name = char.split('.')[0]
        hash_vals[char_name] = hash_val
    
    print(hash_vals.items())
    with open('HashFiles/hash.json', 'w') as fp:
        json.dump(hash_vals, fp)


def get_chars():
    """从截图样本中得到单个字符的图像，用于前期处理"""
    for img_name in os.listdir('Screenshots'):
        img = Image.open(os.path.join('Screenshots', img_name))
        # 此处的值因人而异，只要包含算式区域即可
        img = binarize(img.crop([0, 700, 1080, 1200]))
        h_cut_imgs = horizontal_cut(img)
        char_list1 = vertical_cut(h_cut_imgs[0])
        # char_list2 = vertical_cut(h_cut_imgs[1])
        for char in char_list1:
            char.show()
            pic_name = input('name:')
            if pic_name:
                char.save('Characters/{}.png'.format(pic_name))


def check_location():
    """得到截图并打开，以便观察 config 中设置是否正确"""
    if sys.platform == 'win32':
        from PIL import ImageGrab
        scr = ImageGrab.grab([loc['left_top_x'], loc['left_top_y'], loc['right_buttom_x'], loc['right_buttom_y']])
        # scr.save('screenshot.png')
        scr.show()
        return scr
    elif sys.platform == 'linux':
        cmd = 'import -window root -crop {0}x{1}+{2}+{3} screenshot.png'
        cmd = cmd.format(loc['right_buttom_x'] - loc['left_top_x'], loc['right_buttom_y'] - loc['left_top_y'],
                         loc['left_top_x'], loc['left_top_y'])
        os.system(cmd)
        scr = Image.open('screenshot.png')
        scr.show()
        return scr
    else:
        print('Unsupported platform: ', sys.platform)
        sys.exit()


if __name__ == '__main__':
    """
    --check_location
    --update_hashfile
    """
    if len(sys.argv) > 1:
        if sys.argv[1].startswith('--'):
            option = sys.argv[1][2:]
        else:
            print("Error:")
            print("Wrong argument!")
            print("")
            print("- Run 'python util.py --check_location' to check the equation grabbed from the screenshot.")
            print("- Run 'python util.py --update_hashfile' to update the hashfiles.")
            sys.exit()
        if option == 'check_location':
            check_location()
        elif option == 'update_hashfile':
            get_hashfile()
    else:
        print("Warning:")
        print("No options specified.")
        print("")
        print("- Run 'python util.py check_location' to check the equation grabbed from the screenshot.")
        print("- Run 'python util.py update_hashfile' to update the hashfiles.")

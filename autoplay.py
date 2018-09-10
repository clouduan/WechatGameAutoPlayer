import os
import sys
import time
import traceback
from pymouse import PyMouse
from imgtools import *
from config import location_on_pc as loc


def get_screenshot():
    if sys.platform == 'win32':
        from PIL import ImageGrab
        scr = ImageGrab.grab([loc['left_top_x'], loc['left_top_y'], loc['right_buttom_x'], loc['right_buttom_y']])
        return scr
    elif sys.platform == 'linux':
        cmd = 'import -window root -crop {0}x{1}+{2}+{3} screenshot.png'
        cmd = cmd.format(loc['right_buttom_x'] - loc['left_top_x'], loc['right_buttom_y'] - loc['left_top_y'],
                         loc['left_top_x'], loc['left_top_y'])
        os.system(cmd)
        scr = Image.open('screenshot.png')
        return scr
    else:
        print('Unsupported platform: ', sys.platform)
        sys.exit()


def Play():
    m = PyMouse()
    flag = ""
    loop = 0
    while loop < loops:
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
                loop += 1
        except:
            if 'scr' in vars():
                scr.save('failed.png')
            print("loops: %s" % loop)
            print('Error occurred: ')
            print(traceback.print_exc())
            sys.exit()
        # print('One loop: ', time.perf_counter() - a)


if __name__ == '__main__':
    """
    --loops
    """
    loops = 99999
    if len(sys.argv) == 1:
        Play()
    else:
        if sys.argv[1].startswith('--'):
            loops = int(sys.argv[1].split('=')[1])
            Play()
        else:
            print("Error:")
            print("Wrong argument!")
            print("")
            print("- Run 'python autoplay.py --loops=[number]' to limit the loops.")

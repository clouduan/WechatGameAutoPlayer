from TimeMeasurement import TimeMeasuring
from pymouse import PyMouse
from ImgTools import Recognize
from PIL import Image
from Config import location_on_pc as location
import os
import time
import sys


@TimeMeasuring
def GetScreenshot():
    if sys.platform == 'win32':
        from PIL import ImageGrab
        scr = ImageGrab.grab(
            [location['left_top_x'], location['left_top_y'], location['right_buttom_x'], location['right_buttom_y']])
        return scr
    elif sys.platform == 'linux':
        command = 'import -window root -crop {0}x{1}+{2}+{3} screenshot.png'
        command = command.format(location['right_buttom_x'] - location['left_top_x'],
                                 location['right_buttom_y'] - location['left_top_y'],
                                 location['left_top_x'],
                                 location['left_top_y'])
        os.system(command)
        scr = Image.open('screenshot.png')
        return scr
    else:
        print('Unsupported platform: ', sys.platform)
        os._exit(0)


def Play():
    m = PyMouse()
    flag = ""
    while True:
        a = time.perf_counter()
        time.sleep(0.1)
        try:
            scr = GetScreenshot()
            expr = Recognize(scr)
            print(expr, eval(expr))
            if flag == expr:
                continue
            else:
                flag = expr
                if eval(expr):
                    m.click(location['click_true_x'], location['click_true_y'], 1)
                else:
                    m.click(location['click_false_x'], location['click_false_y'], 1)
        except Exception as e:
            if 'scr' in vars():
                scr.save('failed.png')
            print('Error occurred: ', e)
        print('One loop: ', time.perf_counter() - a)


if __name__ == '__main__':
    Play()

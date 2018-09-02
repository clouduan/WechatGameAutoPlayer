import os
import time
import subprocess
from io import BytesIO

from PIL import Image
import pyscreenshot as ImageGrab
from pymouse import PyMouse
from config import debug


def timing(func):
    def wrap(*args, **kwargs):
        time_flag = time.perf_counter()
        result = func(*args)
        # 显示用时
        if debug:
            print(func.__name__ + ': %.5fs' % (time.perf_counter() - time_flag))
        return result
    
    return wrap


@timing
def get_screenshot_adb_1():
    process = subprocess.Popen('adb shell screencap -p', shell=True, stdout=subprocess.PIPE)
    screenshot = process.stdout.read()
    imgFile = BytesIO(screenshot)
    img = Image.open(imgFile)


@timing
def get_screenshot_adb_2():
    os.system('adb exec-out screencap -p > screenshot.png')
    img = Image.open('screenshot.png')


@timing
def simulate_click_adb():
    os.system('adb shell input tap 300 1500')


@timing
def get_screenshot_linux_1():
    '''
    不支持预选定area
    '''
    im = ImageGrab.grab()


@timing
def get_screenshot_linux_2():
    os.system('import -window root -crop 300x180+100+300 screenshot.png')
    src = Image.open('screenshot.png')
    return src


@timing
def get_screenshot_linux_3():
    '''
    不支持预选定area
        '''
    os.system('scrot screenshot.png')


@timing
def get_screenshot_linux_4():
    '''
    不支持预选定area
    '''
    os.system('gnome-screenshot -f screenshot.png')


@timing
def simulate_click_pc():
    m = PyMouse()
    m.click(150, 650, 1)


@timing
def get_screenshot_windows():
    from PIL import ImageGrab
    img = ImageGrab.grab([100, 100, 400, 400])

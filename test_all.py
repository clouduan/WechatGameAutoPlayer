from ImgTools import *
from Util import *


class Test:
    def test_ImgTools(self):
        scr = Image.open('Screenshots/0th.png')
        scr = scr.crop([0, 700, 1080, 1200])
        assert(Recognize(scr) == '9-5==6')

    def test_GetHashValue(self):
        assert(GetHashValue() == True)

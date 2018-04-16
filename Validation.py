"""
This program aims at choosing the best PHA for recognition.
"""
from pytesseract import image_to_string
from PIL import Image
from Recognize import Recognize
import imagehash
import json
import os


class Validation(Recognize):
    def calc_hash(self, func, funcname):
        """
        Calculate 5 hash values for ONE alphabet.
        Based on perceptual hash algorithms.
        """
        hash_dict = {}
        img_dict = {
            'a': [
                './alphabet_images/a/tmp/0.jpg',
                './alphabet_images/a/tmp/1.jpg',
                './alphabet_images/a/tmp/2.jpg',
                './alphabet_images/a/tmp/3.jpg',
                './alphabet_images/a/tmp/121.jpg',
            ],
            'b': [
                './alphabet_images/b/tmp/2.jpg',
                './alphabet_images/b/tmp/1.jpg',
                './alphabet_images/b/tmp/11.jpg',
                './alphabet_images/b/tmp/22.jpg',
                './alphabet_images/b/tmp/54.jpg',
            ],
            'c': [
                './alphabet_images/c/tmp/0.jpg',
                './alphabet_images/c/tmp/1.jpg',
                './alphabet_images/c/tmp/2.jpg',
                './alphabet_images/c/tmp/4.jpg',
                './alphabet_images/c/tmp/99.jpg',
            ],
            'd': [
                './alphabet_images/d/tmp/0.jpg',
                './alphabet_images/d/tmp/1.jpg',
                './alphabet_images/d/tmp/8.jpg',
                './alphabet_images/d/tmp/25.jpg',
                './alphabet_images/d/tmp/90.jpg',
            ],
            'e': [
                './alphabet_images/e/tmp/4.jpg',
                './alphabet_images/e/tmp/3.jpg',
                './alphabet_images/e/tmp/33.jpg',
                './alphabet_images/e/tmp/39.jpg',
                './alphabet_images/e/tmp/53.jpg',
            ],
            'f': [
                './alphabet_images/f/tmp/0.jpg',
                './alphabet_images/f/tmp/4.jpg',
                './alphabet_images/f/tmp/2.jpg',
                './alphabet_images/f/tmp/39.jpg',
                './alphabet_images/f/tmp/74.jpg',
            ],
            'g': [
                './alphabet_images/g/tmp/2.jpg',
                './alphabet_images/g/tmp/8.jpg',
                './alphabet_images/g/tmp/21.jpg',
                './alphabet_images/g/tmp/39.jpg',
                './alphabet_images/g/tmp/102.jpg',
            ],
            'h': [
                './alphabet_images/h/tmp/0.jpg',
                './alphabet_images/h/tmp/1.jpg',
                './alphabet_images/h/tmp/9.jpg',
                './alphabet_images/h/tmp/12.jpg',
                './alphabet_images/h/tmp/75.jpg',
            ],
            'i': [
                './alphabet_images/i/tmp/0.jpg',
                './alphabet_images/i/tmp/1.jpg',
                './alphabet_images/i/tmp/24.jpg',
                './alphabet_images/i/tmp/27.jpg',
                './alphabet_images/i/tmp/41.jpg',
            ],
            'j': [
                './alphabet_images/j/tmp/0.jpg',
                './alphabet_images/j/tmp/3.jpg',
                './alphabet_images/j/tmp/4.jpg',
                './alphabet_images/j/tmp/5.jpg',
                './alphabet_images/j/tmp/9.jpg',
            ],
            'k': [
                './alphabet_images/k/tmp/0.jpg',
                './alphabet_images/k/tmp/1.jpg',
                './alphabet_images/k/tmp/2.jpg',
                './alphabet_images/k/tmp/3.jpg',
                './alphabet_images/k/tmp/4.jpg',
            ],
            'l': [
                './alphabet_images/l/tmp/0.jpg',
                './alphabet_images/l/tmp/1.jpg',
                './alphabet_images/l/tmp/4.jpg',
                './alphabet_images/l/tmp/28.jpg',
                './alphabet_images/l/tmp/32.jpg',
            ],
            'm': [
                './alphabet_images/m/tmp/0.jpg',
                './alphabet_images/m/tmp/1.jpg',
                './alphabet_images/m/tmp/2.jpg',
                './alphabet_images/m/tmp/3.jpg',
                './alphabet_images/m/tmp/4.jpg',
            ],
            'n': [
                './alphabet_images/n/tmp/0.jpg',
                './alphabet_images/n/tmp/3.jpg',
                './alphabet_images/n/tmp/4.jpg',
                './alphabet_images/n/tmp/5.jpg',
                './alphabet_images/n/tmp/7.jpg',
            ],
            'o': [
                './alphabet_images/o/tmp/2.jpg',
                './alphabet_images/o/tmp/3.jpg',
                './alphabet_images/o/tmp/9.jpg',
                './alphabet_images/o/tmp/10.jpg',
                './alphabet_images/o/tmp/11.jpg',
            ],
            'p': [
                './alphabet_images/p/tmp/0.jpg',
                './alphabet_images/p/tmp/4.jpg',
                './alphabet_images/p/tmp/5.jpg',
                './alphabet_images/p/tmp/6.jpg',
                './alphabet_images/p/tmp/7.jpg',
            ],
            'q': [
                './alphabet_images/q/tmp/0.jpg',
                './alphabet_images/q/tmp/9.jpg',
                './alphabet_images/q/tmp/26.jpg',
                './alphabet_images/q/tmp/20.jpg',
                './alphabet_images/q/tmp/57.jpg',
            ],
            'r': [
                './alphabet_images/r/tmp/1.jpg',
                './alphabet_images/r/tmp/2.jpg',
                './alphabet_images/r/tmp/3.jpg',
                './alphabet_images/r/tmp/4.jpg',
                './alphabet_images/r/tmp/5.jpg',
            ],
            's': [
                './alphabet_images/s/tmp/0.jpg',
                './alphabet_images/s/tmp/1.jpg',
                './alphabet_images/s/tmp/2.jpg',
                './alphabet_images/s/tmp/3.jpg',
                './alphabet_images/s/tmp/4.jpg',
            ],
            't': [
                './alphabet_images/t/tmp/0.jpg',
                './alphabet_images/t/tmp/2.jpg',
                './alphabet_images/t/tmp/13.jpg',
                './alphabet_images/t/tmp/24.jpg',
                './alphabet_images/t/tmp/43.jpg',
            ],
            'u': [
                './alphabet_images/u/tmp/0.jpg',
                './alphabet_images/u/tmp/1.jpg',
                './alphabet_images/u/tmp/13.jpg',
                './alphabet_images/u/tmp/31.jpg',
                './alphabet_images/u/tmp/48.jpg',
            ],
            'v': [
                './alphabet_images/v/tmp/2.jpg',
                './alphabet_images/v/tmp/8.jpg',
                './alphabet_images/v/tmp/16.jpg',
                './alphabet_images/v/tmp/20.jpg',
                './alphabet_images/v/tmp/65.jpg',
            ],
            'w': [
                './alphabet_images/w/tmp/0.jpg',
                './alphabet_images/w/tmp/2.jpg',
                './alphabet_images/w/tmp/3.jpg',
                './alphabet_images/w/tmp/4.jpg',
                './alphabet_images/w/tmp/18.jpg',
            ],
            'x': [
                './alphabet_images/x/tmp/0.jpg',
                './alphabet_images/x/tmp/1.jpg',
                './alphabet_images/x/tmp/2.jpg',
                './alphabet_images/x/tmp/4.jpg',
                './alphabet_images/x/tmp/5.jpg',
            ],
            'y': [
                './alphabet_images/y/tmp/0.jpg',
                './alphabet_images/y/tmp/3.jpg',
                './alphabet_images/y/tmp/4.jpg',
                './alphabet_images/y/tmp/7.jpg',
                './alphabet_images/y/tmp/9.jpg',
            ],
            'z': [
                './alphabet_images/z/tmp/0.jpg',
                './alphabet_images/z/tmp/1.jpg',
                './alphabet_images/z/tmp/3.jpg',
                './alphabet_images/z/tmp/4.jpg',
                './alphabet_images/z/tmp/5.jpg',
            ]
        }
        for alphabet in img_dict:
            hash_dict[alphabet] = []
            for img in img_dict[alphabet]:
                img_hash = str(func(Image.open(img)))
                hash_dict[alphabet].append(img_hash)
        with open('./hash_files/' + funcname + '.json', 'w') as fp:
            json.dump(hash_dict, fp)

    def generate_validation(self):
        """
        Generate validation image-set from raw_images.
        """
        for i in os.listdir('./raw_images')[:100]:
            try:
                img = Image.open('./raw_images/' + i)
                b_img = self.b_process(img)
                captcha = image_to_string(b_img)
                img.save('./validation_images/' + captcha + '.jpg')
            except:
                continue

    def evaluate(self, func, funcname):
        """
        This function aims at evaluating the Accuracy of each hash-function.
        :param func: Hash function
        :param funcname: Hash function name
        :return: ratio
        """
        total = os.listdir('./validation_images')
        corrent = 0
        for img_name in total:
            img = Image.open('./validation_images/' + img_name)
            captcha = self.recognize(img, func, funcname)
            if captcha == img_name[:-4]:
                corrent += 1
        ratio = '%.2f%%' % (corrent / len(total) * 100)
        print(funcname + ': ' + str(corrent) + '/' + str(len(total)) + '  ' + str(ratio))


if __name__ == '__main__':
    valid = Validation()
    # valid.calc_hash(imagehash.whash,'whash')
    # valid.calc_hash(imagehash.average_hash,'ahash')
    # valid.calc_hash(imagehash.dhash,'dhash')
    # valid.calc_hash(imagehash.phash,'phash')
    # valid.calc_hash(valid.bin_ahash,'bin_ahash')

    valid.evaluate(imagehash.average_hash, 'ahash')
    valid.evaluate(imagehash.dhash, 'dhash')
    valid.evaluate(imagehash.phash, 'phash')
    valid.evaluate(imagehash.whash, 'whash')
    valid.evaluate(valid.bin_ahash, 'bin_ahash')

    # img = Image.open('aasd.jpg')
    # print(valid.recognize(img,valid.bin_ahash,'bin_ahash'))

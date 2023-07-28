import time
import cv2
import subprocess

def resizeWithAspectRatio(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv2.resize(image, dim, interpolation=inter)

def standardizeImage(file_path):
    return resizeWithAspectRatio(cv2.imread(file_path), width = 500)

class GoCamera():
    def capture(self):
        temp_picture = './resources/temp_picture.jpg'
        subprocess.run(["raspistill", "-o", temp_picture])
        return standardizeImage(temp_picture)        
        
from picamera import PiCamera
from time import sleep
import numpy as np
import sys
import functools
import cv2
sys.path.insert(1, '/home/pi/G.O.A.T-Project/submodules/watchGo')
import watchGo

class GoCamera:
    def __init__(self, bs):
        self.camera = PiCamera()
        self.board_size = bs
        camera.start_preview(alpha = 192)
        self.frame_size = None

# camera = PiCamera()
# camera.start_preview()
# sleep(1)
# name = "RoyDumb.jpg"
# camera.capture("/home/pi/G.O.A.T-Project/temp/" + name)
# camera.stop_preview()
# camera.close()
# print("hi")
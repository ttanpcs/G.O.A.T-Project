from picamera import PiCamera
from time import sleep
import numpy as np
import functools
import cv2
import watchGo

# class GoCamera:
#     def __init__(self, bs):
#         self.camera = PiCamera()
#         self.board_size = bs
#         camera.start_preview(alpha = 192)
#         self.frame_size = None

camera = PiCamera()
camera.start_preview()
sleep(1)
pre_name = "./resources/preTest.jpg"
post_name = "./resources/postTest.jpg"
camera.capture(pre_name)
a = input("Press a key")
camera.capture(post_name)
camera.stop_preview()
camera.close()
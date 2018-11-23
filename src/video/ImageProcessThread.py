'''
Module: ImageProcessThread.py
Purpose: Processes framedata passed from CaptureThread for further processing before being
         sent to the OCR for image recognition
Depends: Queue, Threading, cv2
'''

import threading
import cv2
import numpy as np
import time

from src.system.graphics import ApplyFilter, applyEdgeFilter, applyBlurFilter, filterType

from PyQt5.QtCore import *
from PyQt5.QtGui import *


class ImageProcessThread(threading.Thread):

    def __init__(self, procQ, detectQ):
        threading.Thread.__init__(self)
        self.ProcessQ = procQ
        self.DetectQ = detectQ
        self.running = True
        self.VidPath = './output.png'


    def run(self):
        self.processFrames()

    def isRunning(self):
        return self.running

    def stop(self):
        self.running = False

    def resume(self):
        self.running = True

    def processFrames(self):
        while self.running:
            if self.ProcessQ.qsize() > 3:
                frame = {}

                nextImage = self.ProcessQ.get()
                #currentImage is considered pure frame data from capture cam
                currentImage = applyEdgeFilter(nextImage)
                frame["img"] = currentImage

                cv2.imwrite(self.VidPath, currentImage)
                self.DetectQ.put(frame)
            else:
                time.sleep(1)



'''
Module: DetectThread.py
Purpose: Processes framedata passed from ImageProcessThread to get check OCR
Depends: Queue, Threading, cv2
'''

import threading
import cv2
import time


class DetectThread(threading.Thread):

    def __init__(self, detectQ):
        threading.Thread.__init__(self)
        self.DetectQueue = detectQ

    def run(self):
        self.detectFrame()

    def isRunning(self):
        return self.running

    def stop(self):
        self.running = False

    def resume(self):
        self.running = True

    def detectFrame(self):
        while self.running:
            if not self.DetectQueue.empty():
                print('Hi')
            else:
                time.sleep(1)


        self.join()

'''
Module: ImageProcessThread.py
Purpose: Processes framedata passed from CaptureThread for further processing before being
         sent to the OCR for image recognition
Depends: Queue, Threading, cv2
'''


import threading
import cv2


class ImageProcessThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        print("PH")

    def isRunning(self):
        return self.running

    def stop(self):
        self.running = False

    def resume(self):
        self.running = True


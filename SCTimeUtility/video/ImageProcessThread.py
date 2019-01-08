'''
Module: ImageProcessThread.py
Purpose: Processes framedata passed from CaptureThread for further processing before being
         sent to the OCR for image recognition
Depends: Queue, Threading, cv2
'''

import threading, cv2, time, numpy as np

from SCTimeUtility.system.Graphics import ApplyFilter, filterType

class ImageProcessThread(threading.Thread):

    def __init__(self, procQ, detectQ, fps, canvas=None):
        threading.Thread.__init__(self)
        self.ProcessQ = procQ
        self.DetectQ = detectQ
        self.running = False
        self.VidPath = './output.png'
        self.canvas = canvas
        self.frames = fps
        self.loopDeltaTime = 1 / self.frames

    def run(self):
        self.processFrames()

    def isRunning(self):
        return self.running

    def stop(self):
        self.running = False

    def resume(self):
        self.running = True

    def processFrames(self):
        # self.running = True
        self.running = False

        # create the kernal and background subtractor
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        fgbg = cv2.createBackgroundSubtractorMOG2()

        #frames needed to calculate if a frame should be added to next queue
        prevFrame = None
        difference = None

        # initalize fps lock based on time
        currentTime = targetTime = time.time()
        while self.running:

            # calculate difference in time and get the current time
            previousTime = currentTime
            currentTime = time.time()
            deltaTime = currentTime - previousTime

            # make sure to run at 3 frames behind capture Thread
            if self.ProcessQ.qsize() > 3:
                nextImage = self.ProcessQ.get()
                currentImage, guiImage = ApplyFilter(nextImage, filterType.EDGE)
                self.DetectQ.put(currentImage)

            # keep adding the difference in time needed and calculate sleep based on that
            targetTime = + self.loopDeltaTime
            sleepAmount = targetTime - time.time()

            if sleepAmount > 0:
                time.sleep(sleepAmount)

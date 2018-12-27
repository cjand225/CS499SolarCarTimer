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
        self.running = False

    def run(self):
        self.detectFrame()

    def isRunning(self):
        return self.running

    def stop(self):
        self.running = False

    def resume(self):
        self.running = True

    def detectFrame(self):
        self.running = False

        # create the kernal and background subtractor
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        fgbg = cv2.createBackgroundSubtractorMOG2()

        while self.running:

            # make sure thread runs 3 frames behind image process thread
            if self.DetectQueue.qsize() > 3:
                next = self.DetectQueue.get()

                # if self.DetectQ.qsize() > 3:
                #     if self.canvas:
                #         #last = self.DetectQ.get()
                #         currentImage = self.DetectQ.get()
                #         fgmask = fgbg.apply(currentImage)
                #         fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)

                #         fg = QImage(fgmask, fgmask.shape[1], fgmask.shape[0], fgmask.strides[0], QImage.Format_Grayscale8)

                #        #cv2.imwrite(self.VidPath, fg)
                #        self.canvas.setPixmap(QPixmap.fromImage(fg))

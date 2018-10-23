'''
Module: UpdateThread.py
Purpose: Thread used for constant and consistent updating of the ImageCanvas gui element that is part of
         the VisionWidget
Depends on: threading, cv2(OpenCv), PyQt5 QImage, ImageCanvas


'''
import threading
import cv2
from PyQt5.QtGui import QImage
from src.video.ImageCanvas import ImageCanvas


class UpdateThread(threading.Thread):

    def __init__(self, Canvas, queue):
        threading.Thread.__init__(self)
        self.iCanvas = Canvas
        self.windowWidth = self.iCanvas.frameSize().width()
        self.windowHeight = self.iCanvas.frameSize().height()
        self.imageQueue = queue
        self.running = True

    def run(self):
        self.updateCanvas()

    def isRunning(self):
        return self.running

    #def getQueue(self):


    def stop(self):
        self.running = False

    def resume(self):
        self.running = True


    '''
        Function: UpdateThread()
        Purpose: grabs captureThread Frame data from imageQueue, does a little preprocessing before updating it to a 
                 final Qimage that is then set as the current image for the ImageCanvas gui element on VisionWidget
        Depends On: ImageCanvas, Queue(imageQueue)
        
    '''
    def updateCanvas(self):
        if not self.imageQueue.empty():
            frame = self.imageQueue.get()
            currentImage = frame["img"]

            imageHeight, imageWidth, imageColors = currentImage.shape
            scaleWidth = float(self.windowWidth) / float(imageWidth)
            scaleHeight = float(self.windowHeight) / float(imageHeight)
            scale = min([scaleWidth, scaleHeight])

            if scale == 0:
                scale = 1

            currentImage = cv2.resize(currentImage, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
            currentImage = cv2.cvtColor(currentImage, cv2.COLOR_BGR2RGB)
            height, width, bpc = currentImage.shape
            bpl = bpc * width

            finalImage = QImage(currentImage.data, width, height, bpl, QImage.Format_RGB888)
            self.iCanvas.setImage(finalImage)


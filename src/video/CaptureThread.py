'''
Module: CaptureThread.py
Purpose: a thread classs intended for retrieving frame data constantly from a video device(webcam),
         and adding that frame data to a queue that is then passed to UpdateThread and ImageProcessThread.
Depends On: threading, cv2(OpenCV)


'''

import threading
import cv2
import time
import numpy as np

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class CaptureThread(threading.Thread):
    '''
        Function: __init__(queue, imageCam, width, height, fps)
        Purpose: Instance of the captureThread, used to prepare thread to capture frame data,
                by specifying the Capture device number through imageCam, the width and height of
                the image(resolution), and the amount of frames per second desired.

    '''

    def __init__(self, queueOne, queueTwo, imageCam, width, height, fps, canvas=None, ):
        threading.Thread.__init__(self)

        self.canvas = canvas
        # variables needed for capturing frame data
        self.captureCam = imageCam  # Specific I/O Device
        self.imageWidth = width  # Resolution Width
        self.imageHeight = height  # Resolution Height
        self.frames = fps  # Frames per Second
        self.CapQ = queueOne  # queue for adding multiple frame
        self.UpQ = queueTwo
        self.running = False
        self.Edge = True
        self.Normal = False


    # executes what the thread is meant for
    def run(self):
        self.grab()

    '''
        Function: isRunning()
        Purpose:  returns a boolean value that indicates if the thread is still running.
    '''

    def isRunning(self):
        return self.running

    '''
        Function: stop()
        Purpose: changes the boolean value of running such that it will terminate the loop in grab function
                 on the next pass (used before joining thread in handler).
    '''

    def stop(self):
        self.running = False

    '''
        Function: grab()
        Purpose: sets a capture device, Frames per second, Height and Width of image,
                 then continously runs by grabbing that specified frame data from the
                 capture device(webcam) and then pushes that onto a queue(stack).
    '''

    # gets frame data continously until thread stops
    def grab(self):
        self.running = True
        capture = cv2.VideoCapture(self.captureCam)
        capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.imageWidth)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.imageHeight)
        capture.set(cv2.CAP_PROP_FPS, self.frames)

        while (self.running):
            frame = {}
            capture.grab()
            retval, img = capture.retrieve(0)
            frame["img"] = img

            #corverts frame to normal image or edge detection image based on boolean setting and returns it
            currentImage, self.newImg = self.ApplyFilter(img)

            # if canvas is actually set, update it
            if self.canvas:
                self.canvas.setPixmap(QPixmap.fromImage(self.newImg))

            self.CapQ.put(img)

        self.join()



    #function works by setting either self.Edge to True or self.Normal to True in the initalizer of the this class
    def ApplyFilter(self, imgData):
        if self.Edge == True:
            edges = self.applyEdgeFilter(imgData)
            return edges, QImage(edges, edges.shape[1], edges.shape[0], edges.strides[0], QImage.Format_Grayscale8)
        elif self.Normal == True:
            Norm = cv2.cvtColor(imgData, cv2.COLOR_BGR2RGB)
            return Norm, QImage(Norm, Norm.shape[1], Norm.shape[0], Norm.strides[0], QImage.Format_RGB888)
        else:
            Norm = cv2.cvtColor(imgData, cv2.COLOR_BGR2RGB)
            return Norm, QImage(Norm, Norm.shape[1], Norm.shape[0], Norm.strides[0], QImage.Format_RGB888)



    def applyEdgeFilter(self, imgData):
        sigma = 0.2
        v = np.median(imgData)
        bilateralImage = cv2.bilateralFilter(imgData, 3, 225, 225)
        hsv = cv2.cvtColor(bilateralImage, cv2.COLOR_BGR2GRAY)
        lower = int(max(0, (1.0 - sigma) * v))
        upper = int(min(255, (1.0 + sigma) * v))
        edges = cv2.Canny(hsv, lower, upper)
        return edges

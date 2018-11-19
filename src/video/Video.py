'''
Module: Video.py
Purpose:

Depends On:
'''

import queue

from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import *

from src.video.VisionWidget import VisionWidget
from src.video.CaptureThread import CaptureThread
from src.video.ImageProcessThread import ImageProcessThread




class Video():

    def __init__(self, uipath):
        self.UIpath = uipath
        self.VisWidget = None

        # device requirements
        self.FramesPerSecond = 60
        self.VidWidth = 1920
        self.VidHeight = 1080
        self.DeviceNum = 0

        self.ImgCanvasWidth = None
        self.ImgCanvasHeight = None

        self.CapThread = None
        self.ProcThread = None
        self.UpThread = None
        self.DetectThread = None
        self.CaptureQ = None
        self.ProcessQ = None
        self.UpdateQ = None

        self.initUI()
        self.initBinds()


    def initUI(self):
        self.VisWidget = VisionWidget(self.UIpath)
        self.ImgCanvasWidth = self.VisWidget.getWidth()
        self.ImgCanvasHeight = self.VisWidget.getHeight()

    def initQueues(self):
        self.CaptureQ = queue.Queue()
        self.UpdateQ = queue.Queue()
        self.ProcessQ = queue.Queue()


    def initThreads(self):
        self.initCapThread()
        self.initProcThread()
        self.initDetectThread()

    def initCapThread(self):
        self.CapThread = CaptureThread(self.CaptureQ, self.UpdateQ, self.DeviceNum,
                                       self.VidWidth, self.VidHeight, self.FramesPerSecond, self.VisWidget.imgCanvas)

    def initProcThread(self):
        self.ProcThread = ImageProcessThread(self.CaptureQ, self.ProcessQ)

    def initDetectThread(self):
        self.DetectThread = None

    def bindStart(self):
        self.VisWidget.getStartButton().clicked.connect(self.startVideo)

    def bindStop(self):
        self.VisWidget.getStopButton().clicked.connect(self.stopVideo)

    def initBinds(self):
        self.bindStart()
        self.bindStop()

    def getWidget(self):
        return self.VisWidget


    def startVideo(self):
        self.initQueues()
        self.initThreads()
        self.CapThread.start()
        self.ProcThread.start()


    def stopVideo(self):
        self.CapThread.stop()
        self.UpThread.stop()

    #def cleanUp(self):


'''
Module: Video.py
Purpose:

Depends On:
'''

import queue

from SCTimeUtility.Video.VideoWidget import VisionWidget
from SCTimeUtility.Video.CaptureThread import CaptureThread
from SCTimeUtility.Video.ImageProcessThread import ImageProcessThread
from SCTimeUtility.Video.DetectionThread import DetectThread
from SCTimeUtility.Video.VideoOptionsWidget import VideoOptionsWidget


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
        self.DetectThread = None

        self.CapturedQ = None
        self.ProcessedQ = None

        self.initUI()
        self.initBinds()

    def initUI(self):
        self.VisWidget = VisionWidget(self.UIpath)
        self.ImgCanvasWidth = self.VisWidget.getWidth()
        self.ImgCanvasHeight = self.VisWidget.getHeight()

    def initQueues(self):
        self.CapturedQ = queue.Queue()
        self.ProcessedQ = queue.Queue()

    def initThreads(self):
        self.initCapThread()
        self.initProcThread()
        self.initDetectThread()

    def initCapThread(self):
        self.CapThread = CaptureThread(self.CapturedQ, self.DeviceNum,
                                       self.VidWidth, self.VidHeight, self.FramesPerSecond, self.VisWidget.imgCanvas)

    def initProcThread(self):
        self.ProcThread = ImageProcessThread(self.CapturedQ, self.ProcessedQ, self.FramesPerSecond,
                                             self.VisWidget.imgCanvas)

    def initDetectThread(self):
        self.DetectThread = DetectThread(self.ProcessedQ)

    def initVideoOptions(self):
        # self.vidOptionsWidget = VideoOptionsWidget()
        print()

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
        self.startThreads()

    def stopVideo(self):
        self.cleanUp()

    def cleanUp(self):
        if self.CapThread.isRunning():
            self.CapThread.stop()
            self.CapThread.join()
        if self.ProcThread.isRunning():
            self.ProcThread.stop()
            self.ProcThread.join()
        if self.DetectThread.isRunning():
            self.DetectThread.stop()
            self.DetectThread.join()
        self.VisWidget.clearCanvas()

    def startThreads(self):
        self.CapThread.start()
        self.ProcThread.start()
        self.DetectThread.start()

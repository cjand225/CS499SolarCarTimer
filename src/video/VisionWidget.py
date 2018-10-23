'''
Module: VisionWidget.py
Purpose: A gui element that handles an ImageCanvas that constantly updates to show a video feed
         from a webcam. Inherits from QWidget, Gui elements are mostly pulled from ui file used from Qt4Designer
Depends on: ImageCanvas.py, CaptureThread.py

TODO: Integrate into Video Module, seperate updating to UpdateThread Class, decouple from logic elements

'''


from PyQt5.QtWidgets import QWidget, QGridLayout, QStyle, QApplication, QPushButton
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi
import queue
import cv2

from video.ImageCanvas import ImageCanvas
from video.CaptureThread import CaptureThread

class VisionWidget(QWidget):

    def __init__(self):
        super().__init__()
        #video part
        self.image = None

        # default sizing for Widget
        self.width = self.frameSize().width()
        self.height = self.frameSize().height()
        self.layout = QGridLayout()  # Defines Layout - grid

        #thread related - default
        self.resolution = [None] * 2
        self.fps = None
        self.deviceCam = None
        self.captureThread = None

        #adding list of threads before they are instanced
        #self.threadList = [None] * 4

        #Image queue for capture thread
        self.imageQueue = queue.Queue()

        #self.captureQueue = queue.Queue()
        #self.updateQueue = queue.Queue()
        #self.processQueue = queue.Queue()

        #gives context to capture thread
        self.setDevice(0)
        self.setResolution(1920,1080)
        self.setFps(60)


        #initalizers
        self.initUI()
        self.initButton()
        self.initVisionWidget()




    '''
        Function:  initUI()
        Purpose:  loads most gui elements from a file made in Qt4Designer
        Depends on: Video.ui
    '''
    def initUI(self):
        self.ui = loadUi('./../resources/Video.ui', self)
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignVCenter,
                                            self.size(), QApplication.desktop().availableGeometry()))

    '''
        Function: initVisionWidget()
        Purpose: Instances the imageWidget, sets the windowHeight and windowHeight for later use, adds the ImageCanvas
                 to the layout of the gui named "imageLayout"
        Depends on: ImageCanvas
    '''
    def initVisionWidget(self):
        self.imageWidget = ImageCanvas()
        self.windowWidth = self.imageWidget.frameSize().width()
        self.windowHeight = self.imageWidget.frameSize().height()
        self.imageLayout.addWidget(self.imageWidget)

    '''
        Function: initButton()
        Purpose: Binds buttons on widget gui such that they correspond to the start and stop of the CaptureThread
        Depends on: QButton, Video.ui
    '''
    def initButton(self):
        self.startButton.clicked.connect(self.startThread)
        self.stopButton.clicked.connect(self.stopThread)

    '''
        Function: initCaptureThread()
        Purpose: Creates a captureThread based on variables set before its creation.
        Depends on: imageQueue, deviceCam, resolution[], fps
        
        TODO: Ensure all variables needed are set before creation
    '''
    #initalizes thread for grabbing data from capture cam
    def initCaptureThread(self):
        self.captureThread = CaptureThread(self.imageQueue, self.deviceCam, self.resolution[0], self.resolution[1], self.fps)


    '''
        Function: setResolution(height, width)
        Purpose: sets the resolution of the image for ImageCanvas before 
        Depends on:
    '''
    def setResolution(self, height, width):
        self.resolution[0] = height
        self.resolution[1] = width


    '''
        Function: setFps(frames)
        Purpose: sets a variable called fps in the class VisionWidget for later use when creating a captureThread
                 instance.
    '''
    def setFps(self, frames):
        self.fps = frames

    '''
        Function: setDevice(deviceNum)
        Purpose:  sets a variable called deviceCam in the class VisionWidget for later use when creating
                 a captureThread Instance.
    '''
    def setDevice(self, deviceNum):
        self.deviceCam = deviceNum

    '''
        Function: getCanvas()
        Purpose: Returns a reference to imageCanvas class stored within the VisionWidget
        
    '''
    def getCanvas(self):
        return self.imageWidget

    '''
        Function: startThread()
        Purpose: Ensures creation of CaptureThread, Creation of QTimer used to update ImageCanvas with current frames,
                 and ensures to run the CaptureThread.
                 
        Depends on: CaptureThread, QTimer
    '''
    def startThread(self):
        self.initCaptureThread()
        self.initTimer()
        self.captureThread.start()

    '''
        Function: stopThread()
        Purpose: Ensures that if there is a running CaptureThread, the function attempts to tell the thread to stop
                 and then waits for it to join, then reports via print statement if the thread is still alive or has 
                 sucessfully stopped
    '''
    def stopThread(self):
        if(self.captureThread.isRunning()):
            self.captureThread.stop()
            self.captureThread.join()
            if(self.captureThread.isAlive()):
                print("Thread is still Alive.")
            else:
                print("Thread has Quit.")



    '''
        Function: closeEvent(self, QCloseEvent)
        Purpose:  Overrides the close event that is defined in PyQt5's library to ensure that threads
                    have stopped once the widget has closed.
        Depends on: CaptureThread
    
    '''
    def closeEvent(self, a0: QCloseEvent):
        if(self.captureThread != None and self.captureThread.isRunning()):
            self.stopThread()
        a0.ignore()
        self.hide()

    '''
        Function: UpdateFrame
        Purpose: To update the ImageCanvas class (called imageWidget) with QImage data,
                based on a timer that ticks every second.
                
        TODO: make into seperate thread class that will update with a continous loop that
              will sleep for a few millisecond after each frame to achieve better performance.
    '''
    def updateFrame(self):
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

            self.imageWidget.setImage(finalImage)


    '''
        Function: initTimer()
        Purpose: Initalizes the Qtimer related to calling the updateFrame function, makes sure that the timer
                 starts and ticks every 1 second.
    
    '''
    def initTimer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateFrame)
        self.timer.start(1)



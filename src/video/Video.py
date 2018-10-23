'''
Module: Video.py
Purpose: Encompasses the entirety of vision related aspects of the program, its the controller that
         manages each thread used for Capturing, updating, and processing frames. Enables talking from
         one thread to another by use of the Queue class to add frame data that will be added at the end of one
         frame to be used at the beginning of another thread.

Depends On: CaptureThread.py,UpdateThread.py, ImageProcessThread.py, VisionWidget.py
'''

from src.video.VisionWidget import VisionWidget
from src.video.CaptureThread import CaptureThread
from src.video.UpdateThread import UpdateThread
from src.video.ImageProcessThread import ImageProcessThread


class Video():

    def __init__(self):
       print("PH")


    def initWidget(self):
        print("PH")

    def initCaptureThread(self):
        print("PH")

    def initUpdateThread(self):
        print("PH")

    def initImageProcessThread(self):
        print("PH")
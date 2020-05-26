"""

    Module: DetectThread.py
    Purpose: Processes frame-data passed from ImageProcessThread to get check OCR
    Depends: Queue, Threading, cv2

"""
# Standard Lib Imports
import threading, time

# Dependency Imports
import cv2


class DetectThread(threading.Thread):
    '''

        Function: __init__
        Parameters: self, detectQ=(Queue.queue)
        Return Value: N/A
        Purpose: Initializes a thread used for detecting objects within the images

    '''

    def __init__(self, detection_resource_queue):
        threading.Thread.__init__(self)
        self.detection_queue = detection_resource_queue
        self.running = False

    '''

        Function: run
        Parameters: self
        Return Value: N/A
        Purpose: used to continually run a specific function

    '''

    def run(self):
        self.detection_frame()

    '''

        Function: isRunning
        Parameters: self
        Return Value: Boolean
        Purpose: Returns a boolean value on whether or not the thread is running

    '''

    def is_running(self):
        return self.running

    '''

        Function: stop
        Parameters: self
        Return Value: N/A
        Purpose: Toggles boolean self.running to false to stop thread

    '''

    def stop(self):
        self.running = False

    '''

        Function: start
        Parameters: self
        Return Value: N/A
        Purpose: Toggles boolean self.running to true to run thread

    '''

    def resume(self):
        self.running = True

    '''

        Function: detectFrame
        Parameters: self
        Return Value: N/A
        Purpose: Continually read Queue frame data to detect objects.

    '''

    def detection_frame(self):
        self.running = False

        # create the kernel and background subtraction
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        fgbg = cv2.createBackgroundSubtractorMOG2()

        while self.running:

            # make sure thread runs 3 frames behind image process thread
            if self.detection_queue.qsize() > 3:
                next = self.detection_queue.get()

'''
Module: CaptureThread.py
Purpose: a thread classs intended for retrieving frame data constantly from a video device(webcam),
         and adding that frame data to a queue that is then passed to UpdateThread and ImageProcessThread.
Depends On: threading, cv2(OpenCV)

TODO: pass two seperate queues, one for updateThread, one for ImageProcessThread

'''

import threading
import cv2

class CaptureThread(threading.Thread):


    '''
        Function: __init__(queue, imageCam, width, height, fps)
        Purpose: Instance of the captureThread, used to prepare thread to capture frame data,
                by specifying the Capture device number through imageCam, the width and height of
                the image(resolution), and the amount of frames per second desired.

    '''
    def __init__(self, queue, imageCam, width, height, fps):
        threading.Thread.__init__(self)

        #variables needed for capturing frame data
        self.captureCam = imageCam  #Specific I/O Device
        self.imageWidth = width     #Resolution Width
        self.imageHeight = height   #Resolution Height
        self.frames = fps           #Frames per Second
        self.imageQ = queue         #queue for adding multiple frame
        self.captureThread = None   #
        self.running = False


    #executes what the thread is meant for
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


    def resume(self):
        self.running = True

    #def pause(self):


    '''
        Function: grab()
        Purpose: sets a capture device, Frames per second, Height and Width of image,
                 then continously runs by grabbing that specified frame data from the
                 capture device(webcam) and then pushes that onto a queue(stack).
    '''
    #gets frame data continously until thread stops
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

            if self.imageQ.qsize() < 10:
                self.imageQ.put(frame)
            else:
                print(self.imageQ.qsize()) #frame stack full and/or no camera



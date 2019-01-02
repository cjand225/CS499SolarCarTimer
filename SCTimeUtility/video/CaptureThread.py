'''
Module: CaptureThread.py
Purpose: a thread class intended for retrieving frame data constantly from a video device(webcam),
         and adding that frame data to a queue that is then passed to ImageProcessThread.
Depends On: threading, cv2(OpenCV)


'''

import threading, cv2, time

from PyQt5.QtGui import QPixmap

from SCTimeUtility.system.Graphics import ApplyFilter, filterType


class CaptureThread(threading.Thread):
    '''
        Function: __init__(queue, imageCam, width, height, fps)
        Purpose: Instance of the captureThread, used to prepare thread to capture frame data,
                by specifying the Capture device number through imageCam, the width and height of
                the image(resolution), and the amount of frames per second desired.

    '''

    def __init__(self, queueOne, imageCam, width, height, fps, canvas=None, ):
        threading.Thread.__init__(self)

        self.canvas = canvas
        self.running = False
        self.enableFPS = False

        # variables needed for capturing frame data
        self.captureCam = imageCam  # Specific I/O Device
        self.imageWidth = width  # Resolution Width
        self.imageHeight = height  # Resolution Height
        self.frames = fps  # Frames per Second
        self.CapQ = queueOne  # queue for adding multiple frame
        self.loopDeltaTime = 1 / self.frames

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

    # gets frame data continuously until thread stops
    def grab(self):
        self.running = True

        capture = cv2.VideoCapture(self.captureCam)
        capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.imageWidth)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.imageHeight)
        capture.set(cv2.CAP_PROP_FPS, self.frames)
        capture.open(self.captureCam)

        # set initial target/current times
        guiImage = None
        currentTime = targetTime = time.time()
        while (self.running):
            # calculate difference in time and get the current time
            previousTime = currentTime
            currentTime = time.time()
            deltaTime = currentTime - previousTime

            capture.grab()
            retval, img = capture.retrieve(0)
            # self.showFPS(deltaTime)

            if img is not None:
                retImg, guiImage = ApplyFilter(img, filterType.EDGE)

            if self.canvas:
                self.canvas.setPixmap(QPixmap.fromImage(guiImage))
            self.CapQ.put(img)

            # keep adding the difference in time needed and calculate sleep based on that
            targetTime = + self.loopDeltaTime
            sleepAmount = targetTime - time.time()

            if sleepAmount > 0:
                time.sleep(sleepAmount)

        capture.release()

    def showFPS(self, timeDiff):
        print('FPS: %d' % (1 / timeDiff))
        return

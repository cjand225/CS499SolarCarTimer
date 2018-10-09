import threading
import cv2

class CaptureThread(threading.Thread):

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


    #used to check if thread is running
    def isRunning(self):
        return self.running

    def stop(self):
        self.running = False

    def resume(self):
        self.running = True

    #def pause(self):

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



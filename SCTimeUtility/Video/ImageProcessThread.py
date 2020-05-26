"""

    Module: ImageProcessThread.py
    Purpose: Processes framedata passed from CaptureThread for further processing before being
             sent to the OCR for image recognition
    Depends: Queue, Threading, cv2

"""

# Standard Lib Imports
import threading, time

# Dependency Imports
import numpy as np, cv2

# Package Imports
from SCTimeUtility.System.Graphics import apply_filtering, FilterType


class ImageProcessThread(threading.Thread):

    def __init__(self, process_resource_queue, detection_resource_queue, fps, canvas=None):
        threading.Thread.__init__(self)
        self.frame_process_queue = process_resource_queue
        self.frame_detection_queue = detection_resource_queue
        self.running = False
        self.video_path = './output.png'
        self.canvas = canvas
        self.frames = fps
        self.delta_time_loop = 1 / self.frames

    def run(self):
        self.processFrames()

    def is_running(self):
        return self.running

    def stop(self):
        self.running = False

    def resume(self):
        self.running = True

    def processFrames(self):
        # self.running = True
        self.running = False

        # create the kernal and background subtractor
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        fgbg = cv2.createBackgroundSubtractorMOG2()

        # frames needed to calculate if a frame should be added to next queue
        prev_frame = None
        difference = None

        # initialize fps lock based on time
        current_time = target_time = time.time()
        while self.running:

            # calculate difference in time and get the current time
            previous_time = current_time
            current_time = time.time()
            delta_time = current_time - previous_time

            # make sure to run at 3 frames behind capture Thread
            if self.frame_process_queue.qsize() > 3:
                next_image = self.frame_process_queue.get()
                current_image, gui_image = apply_filtering(next_image, FilterType.EDGE)
                self.frame_detection_queue.put(current_image)

            # keep adding the difference in time needed and calculate sleep based on that
            target_time = + self.delta_time_loop
            sleep_amount = target_time - time.time()

            if sleep_amount > 0:
                time.sleep(sleep_amount)

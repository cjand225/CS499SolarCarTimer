"""

    Module: CaptureThread.py
    Purpose: a thread class intended for retrieving frame data constantly from a Video device(webcam),
             and adding that frame data to a queue that is then passed to ImageProcessThread.
    Depends On: threading, cv2(OpenCV), PyQt, SCT Graphics Module

"""

import threading, cv2, time

from PyQt5.QtGui import QPixmap

from SCTimeUtility.System.Graphics import apply_filtering, FilterType


class CaptureThread(threading.Thread):
    '''
        Function: __init__(queue, imageCam, width, height, fps)
        Purpose: Instance of the captureThread, used to prepare thread to capture frame data,
                by specifying the Capture device number through imageCam, the width and height of
                the image(resolution), and the amount of frames per second desired.

    '''

    def __init__(self, capture_resource_queue, image_device_num, capture_width, capture_height, fps, canvas=None):
        threading.Thread.__init__(self)

        self.canvas = canvas
        self.running = False
        self.enableFPS = False

        # variables needed for capturing frame data
        self.capture_cam = image_device_num  # Specific I/O Device
        self.frame_width = capture_width  # Resolution Width
        self.frame_height = capture_height  # Resolution Height
        self.frame_amount = fps  # Frames per Second
        self.capture_queue = capture_resource_queue  # queue for adding multiple frame
        self.delta_time_loop = 1 / self.frame_amount

    # executes what the thread is meant for
    def run(self):
        self.capture_frames()

    '''
        Function: isRunning()
        Purpose:  returns a boolean value that indicates if the thread is still running.
    '''

    def is_running(self):
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
        Parameters: self
        Return Value: N/A
        Purpose: sets a capture device, Frames per second, Height and Width of image,
                 then continously runs by grabbing that specified frame data from the
                 capture device(webcam) and then pushes that onto a queue(stack).
    '''

    # gets frame data continuously until thread stops
    def capture_frames(self):
        self.running = True

        capture = cv2.VideoCapture(self.capture_cam)
        capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.frame_width)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.frame_height)
        capture.set(cv2.CAP_PROP_FPS, self.frame_amount)
        capture.open(self.capture_cam)

        # set initial target/current times
        canvas_image = None
        current_time = target_time = time.time()
        while (self.running):
            # calculate difference in time and get the current time
            previous_time = current_time
            current_time = time.time()
            delta_time = current_time - previous_time

            capture.grab()
            ret_val, frame_data = capture.retrieve(0)
            # self.display_fps(delta_time)

            if frame_data is not None:
                ret_img, canvas_image = apply_filtering(frame_data, FilterType.EDGE)

            if self.canvas:
                self.canvas.setPixmap(QPixmap.fromImage(canvas_image))
            self.capture_queue.put(frame_data)

            # keep adding the difference in time needed and calculate sleep based on that
            target_time = + self.delta_time_loop
            sleep_amount = target_time - time.time()

            if sleep_amount > 0:
                time.sleep(sleep_amount)

        capture.release()

    '''
    
        Function: showFPS
        Parameters: self, timeDiff
        Return Value: N/A
        Purpose: Shows the current fps of the cam printed out to console.
        
    '''

    def display_fps(self, time_difference):
        print('FPS: %d' % (1 / time_difference))
        return

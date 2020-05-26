"""

    Module:
    Purpose:
    Depends On:

"""

# Standard Lib Imports
import queue

# Package Imports
from SCTimeUtility.Video import videoUIPath
from SCTimeUtility.Video.VideoWidget import VideoWidget
from SCTimeUtility.Video.CaptureThread import CaptureThread
from SCTimeUtility.Video.ImageProcessThread import ImageProcessThread
from SCTimeUtility.Video.DetectionThread import DetectThread
from SCTimeUtility.Video.VideoOptionsWidget import VideoOptionsWidget


class Video:

    def __init__(self):
        self.vision_widget = None

        # device requirements
        self.video_frames_per_second = 60
        self.video_frame_width = 1920
        self.video_frame_height = 1080
        self.device_number = 0

        self.image_canvas_width = None
        self.image_canvas_height = None

        self.frame_capture_thread = None
        self.image_process_thread = None
        self.object_detection_thread = None

        self.frame_capture_queue = None
        self.processed_frames_queue = None

        self.init_widgets()
        self.init_bindings()

    def init_widgets(self):
        self.vision_widget = VideoWidget(videoUIPath)
        self.image_canvas_width = self.vision_widget.get_width()
        self.image_canvas_height = self.vision_widget.get_height()

    def init_resource_queues(self):
        self.frame_capture_queue = queue.Queue()
        self.processed_frames_queue = queue.Queue()

    def init_thread_setup(self):
        self.init_capture_thread()
        self.init_process_thread()
        self.init_detection_thread()

    def init_capture_thread(self):
        self.frame_capture_thread = CaptureThread(self.frame_capture_queue, self.device_number,
                                                  self.video_frame_width, self.video_frame_height, self.video_frames_per_second, self.vision_widget.img_canvas)

    def init_process_thread(self):
        self.image_process_thread = ImageProcessThread(self.frame_capture_queue, self.processed_frames_queue, self.video_frames_per_second,
                                                       self.vision_widget.img_canvas)

    def init_detection_thread(self):
        self.object_detection_thread = DetectThread(self.processed_frames_queue)

    def init_video_options(self):
        pass

    def bind_start_action(self):
        self.vision_widget.get_start_button().clicked.connect(self.start_video)

    def bind_stop_action(self):
        self.vision_widget.get_stop_button().clicked.connect(self.stop_video)

    def init_bindings(self):
        self.bind_start_action()
        self.bind_stop_action()

    def get_widget(self):
        return self.vision_widget

    def start_video(self):
        self.init_resource_queues()
        self.init_thread_setup()
        self.start_threads()

    def stop_video(self):
        self.clean_up()

    def clean_up(self):
        if self.frame_capture_thread.is_running():
            self.frame_capture_thread.stop()
            self.frame_capture_thread.join()
        if self.image_process_thread.is_running():
            self.image_process_thread.stop()
            self.image_process_thread.join()
        if self.object_detection_thread.is_running():
            self.object_detection_thread.stop()
            self.object_detection_thread.join()
        self.vision_widget.clear_canvas()

    def start_threads(self):
        self.frame_capture_thread.start()
        self.image_process_thread.start()
        self.object_detection_thread.start()


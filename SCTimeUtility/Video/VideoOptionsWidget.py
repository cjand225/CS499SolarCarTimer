"""

    Module:
    Purpose:
    Depends On:

"""


from PyQt5.QtWidgets import QWidget, QStyle, QApplication
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi


class VideoOptionsWidget(QWidget):

    def __init__(self, resource_path):
        super().__init__()
        self.resource_path = resource_path

        self.device_num = None
        self.device_list = []
        self.resolution = [None, None]
        self.fps = None

        self.init_widget()

    def init_widget(self):
        self.widget = loadUi(self.resource_path, self)
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignRight,
                                            self.size(), QApplication.desktop().availableGeometry()))

    # try opencv open to find which cameras are connected

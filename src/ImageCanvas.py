from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class ImageCanvas(QWidget):

    def __init__(self):
        super().__init__()
        self.image = None

    def setImage(self, image):
        self.image = image
        imageSize = image.size()
        self.setMinimumSize(imageSize)
        self.update()

    def paintEvent(self, paintEvent):
        canvasPainter = QPainter()
        canvasPainter.begin(self)
        if self.image:
            canvasPainter.drawImage(QPoint(0, 0), self.image)
        canvasPainter.end()

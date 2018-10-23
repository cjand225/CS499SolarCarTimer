'''
Module: ImageCanvas.py
Purpose: a Blank Qwidget used as a canvas in which to draw our Qimage(made in UpdateThread class) allows setting the current
        image and painting that image onto the widget itself, part of the VisionWidget used for camera feed.
Depends On: QWidget, QPainter, QImage

'''


from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class ImageCanvas(QWidget):

    def __init__(self):
        super().__init__()
        self.image = None

    '''
        Function: setImage(image)
        Purpose:  sets the current image to an internal variable (image), updates the minimum size of the canvas based on the
                 size of the image being set, and then updates the ImageCanvas.
    '''
    def setImage(self, image):
        self.image = image
        imageSize = image.size()
        self.setMinimumSize(imageSize)
        self.update()

    '''
        Function: paintEvent(paintEvent)
        Purpose: Overloads paint event in the PyQt5 library such that it draws our image on the widget repeatedly or
                 ends if no image exists.
    '''
    def paintEvent(self, paintEvent):
        canvasPainter = QPainter()
        canvasPainter.begin(self)
        if self.image:
            canvasPainter.drawImage(QPoint(0, 0), self.image)
        canvasPainter.end()

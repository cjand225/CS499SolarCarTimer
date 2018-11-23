"""
    Module: Graphics.py
    Purpose: Related graphics functions kept here for use in various parts of video module

"""
import cv2
import numpy as np
from enum import Enum
from PyQt5.QtGui import QImage

class filterType(Enum):
    NORMAL = 0
    BLUR = 1
    EDGE = 2


def applyEdgeFilter(imgData):
    sigma = 0.33
    v = np.median(imgData)
    bilateralImage = cv2.bilateralFilter(imgData, 3, 225, 225)
    hsv = cv2.cvtColor(bilateralImage, cv2.COLOR_BGR2GRAY)
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edges = cv2.Canny(hsv, lower, upper)
    return edges

def applyBlurFilter(imgData):
    blurImg = cv2.bilateralFilter(imgData, 3, 225, 225)
    return blurImg

def ApplyFilter(imgData, filter):
    if filter == filterType.EDGE:
        edges = applyEdgeFilter(imgData)
        return edges, QImage(edges, edges.shape[1], edges.shape[0], edges.strides[0], QImage.Format_Grayscale8)
    elif filter == filterType.BLUR:
        blur = applyBlurFilter(imgData)
        return blur, QImage(blur, blur.shape[1], blur.shape[0], blur.strides[0], QImage.Format_RGB888)
    elif filter == filterType.NORMAL:
        Norm = cv2.cvtColor(imgData, cv2.COLOR_BGR2RGB)
        return Norm, QImage(Norm, Norm.shape[1], Norm.shape[0], Norm.strides[0], QImage.Format_RGB888)

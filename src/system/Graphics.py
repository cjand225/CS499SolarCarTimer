"""
    Module: Graphics.py
    Purpose: Related graphics functions kept here for use in various parts of video module

"""
import cv2
import numpy as np
from enum import Enum
from PyQt5.QtGui import QImage

"""
    Function: filterType (Class)
    Parameters: N/A
    Return Value: N/A
    Purpose: An enumeration used for ApplyFilter function and allows the invoker to specify what type of
             filter they would like to apply to an image without having multiple function calls, mostly
             used in capture thread for debugging gui related functions when updating gui from cam capture
    
"""


class filterType(Enum):
    NORMAL = 0
    BLUR = 1
    EDGE = 2


"""
    Function: applyEdgeFilter
    Parameters: imgData (Capture Data from opencv cam source)
    Return Value: Altered Image Dict
    Purpose: Takes in Image data from opencv capture cam and mathematically applies a bilateral blur with a kernal size 
            of 3, converts the image from opencv color to grayscale, applies canny edge detection and returns the image
            data to be used however the invoker sees fit. 

"""


def applyEdgeFilter(imgData):
    v = np.median(imgData)
    sigma = 0.33
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    kernalSize = 1

    bilateralImage = cv2.bilateralFilter(imgData, kernalSize, 225, 225)
    hsv = cv2.cvtColor(bilateralImage, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(hsv, lower, upper)

    return edges


"""
    Function: applyBlurFilter
    Parameters: imgData
    Return Value: Modified imgData
    Purpose: Applies a bilateral filtering with a size 3 kernal with a sigma space of 225 and a max sigma color of
             225

"""


def applyBlurFilter(imgData):
    blurImg = cv2.bilateralFilter(imgData, 3, 225, 225)
    blur = cv2.cvtColor(blurImg, cv2.COLOR_BGR2RGB)
    return blur


"""
    Function: ApplyFilter
    Parameters: imgData, FilterType Enum
    Return Value: modified imgData, QImage
    Purpose: Applies filtering on imgData based on the Enumeration given from FilterType class and when processed
             returns a modified imgData as well as a QImage mainly used for updating vision widget.

"""


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

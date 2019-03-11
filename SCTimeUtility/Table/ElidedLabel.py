'''
Module: ElidedLabel.py
Purpose:

Depends On:
'''
from PyQt5.Qt import pyqtProperty
from PyQt5.QtCore import Qt, pyqtSignal, pyqtBoundSignal
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QFontMetrics, QPainter, QTextLayout
from SCTimeUtility.Log.Log import getLog


class ElidedLabel(QLabel):

    def __init__(self, text=""):
        super().__init__()
        self._elided = False
        self.content = text

    '''  
        Function: elided
        Parameters: self
        Return Value: self._elided
        Purpose: PyQt property declared for used of the ElidedLabel class
    '''

    @pyqtProperty(bool)
    def elided(self):
        return self._elided

    '''  
        Function: paintEvent
        Parameters: self, event
        Return Value: N/A
        Purpose: Overloaded the paintEven function of PyQt to allow the label to work as intended and allow
                 "sliding" of label text.
    '''

    def paintEvent(self, event):
        painter = QPainter(self)
        fontMetrics = painter.fontMetrics()
        elidedText = fontMetrics.elidedText(self.text(), Qt.ElideRight, self.width())
        self._elided = (elidedText != self.text())
        painter.drawText(self.rect(), self.alignment(), elidedText)

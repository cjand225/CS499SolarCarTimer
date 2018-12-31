'''
Module: ElidedLabel.py
Purpose:

Depends On:
'''
from PyQt5.QtCore import Qt, pyqtProperty, pyqtSignal
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QFontMetrics, QPainter, QTextLayout
from SCTimeUtility.log.Log import getInfoLog, getCriticalLog, getDebugLog, getErrorLog, getWarningLog


class ElidedLabel(QLabel):

    def __init__(self, text=""):
        super().__init__()
        self._elided = False
        self.content = text

    @pyqtProperty(bool)
    def elided(self):
        return self._elided

    def paintEvent(self, event):
        painter = QPainter(self)
        fontMetrics = painter.fontMetrics()
        elidedText = fontMetrics.elidedText(self.text(), Qt.ElideRight, self.width())
        self._elided = (elidedText != self.text())
        painter.drawText(self.rect(), self.alignment(), elidedText)

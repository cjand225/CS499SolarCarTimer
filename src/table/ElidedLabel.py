from PyQt5.QtCore import QPoint, Qt, pyqtProperty, pyqtSignal
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QFontMetrics, QPainter, QTextLayout


class ElidedLabel(QLabel):

    def __init__(self, parent, text=""):
        super().__init__(parent)
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

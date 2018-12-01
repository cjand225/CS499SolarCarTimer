from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi


class ElidedLabelTestWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.ui = loadUi("resources/ElidedLabelTestWidget.ui", self)

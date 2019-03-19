"""

    Module:
    Purpose:
    Depends On:

"""

from PyQt5.QtWidgets import QWidget


class Plot(QWidget):

    def __init__(self, parent=None):
        super(Plot, self).__init__(parent)

    def createPlot(self):
        pass

    def removePlot(self):
        pass

    def setAxis(self, x, y):
        pass

    def createLegend(self, legendList):
        pass

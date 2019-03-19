"""

    Module:
    Purpose:
    Depends On:

"""

from PyQt5.QtWidgets import QWidget, QTabWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib import pyplot


class GraphWidget(QWidget):

    def __init__(self):
        super(GraphWidget, self).__init__()
        self.GraphTabs = QTabWidget()

    def initUI(self):
        pass

    def addPlot(self, plot):
        pass

    def removePlot(self, plotIndex):
        pass

    def editPlot(self, plotIndex):
        pass

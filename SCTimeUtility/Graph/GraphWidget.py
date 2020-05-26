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

    def init_widget(self):
        pass

    def add_plot(self, index):
        pass

    def remove_plot(self, index):
        pass

    def edit_plot(self, index):
        pass

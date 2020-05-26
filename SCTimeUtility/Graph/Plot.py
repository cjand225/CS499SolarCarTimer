"""

    Module:
    Purpose:
    Depends On:

"""

from PyQt5.QtWidgets import QWidget


class Plot(QWidget):

    def __init__(self, parent=None):
        super(Plot, self).__init__(parent)

    def create_plot(self):
        pass

    def remove_plot(self):
        pass

    def set_axis(self, x, y):
        pass

    def create_legend(self, legend_list):
        pass

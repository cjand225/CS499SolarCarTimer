from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi


from table.Table import Table
from table.SemiAutoWidget import SemiAutoWidget
from video.VisionWidget import VisionWidget
from table.LogWidget import LogWidget
from graph.GraphOptions import GraphOptions
from graph.Graph import Graph

class AppWindow(QMainWindow):

    def __init__(self):
        super(AppWindow, self).__init__()
        # initialize Window
        self.initMainWindow()

        # setup Menu Bar
        #self.initMainMenu()

        # setup widgets

        self.initButtonWidget()
        self.initVisionWidget()
        self.initLogWidget()
        self.initTableWidget()
        #self.initGraphWidget()

        # initialize gui
        self.initUi()

    def initMainWindow(self):
        self.mainWindowUI = loadUi('./../resources/App.ui', self)
        self.setAttribute(Qt.WA_DeleteOnClose)
        #centers window
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignHCenter,
                                            self.size(), QApplication.desktop().availableGeometry()))


    # Overloads closeEvent function to define what happens when main window X is clicked
    def closeEvent(self, a0: QCloseEvent):
         self.initCloseDialog()
         retval = self.msg.exec()  #grabs event code from Message box execution
         if retval == 1:    #if OK clicked - Close
             a0.accept()
             self.mTable.close()
             self.mButton.close()
             self.mVision.close()
             self.mLog.close()
             self.close()
         #if Cancel or MessageBox is closed - Ignore the signal
         if retval == 0:
             a0.ignore()

    def close(self):
        exit(0)

    def initCloseDialog(self):
        self.msg = QDialog()
        self.msg.ui = loadUi('./../resources/QuitDialog.ui', self.msg)


    #def initMainMenu(self):


    # Initalize/show ui components here
    def initUi(self):
        self.show()

    # handles TableWidget stuff
    def initTableWidget(self):
        self.mTable = Table()

    def initButtonWidget(self):
        self.mButton = SemiAutoWidget()

    def initVisionWidget(self):
        self.mVision = VisionWidget()

    def initLogWidget(self):
        self.mLog = LogWidget()

    def initGraphWidget(self):
        self.mGraphOptions = GraphOptions()
        self.mGraph = Graph()

    #placeholder function
    def handleFileMenu(self, action):
        print("hi")

    # placeholder function
    def handleEditMenu(self, action):
        print("hi")

    def handleViewMenu(self, action):
        if action.text() == "Table":
            self.toggleTableWidget()
        if action.text() == "Log":
            self.toggleLogWidget()
        if action.text() == "Semi-Auto":
            self.toggleButtonWidget()
        if action.text() == "Auto":
            self.toggleVisionWidget()

    # placeholder function
    def handleHelpMenu(self, action):
        print("hi")

    #---------Widget Toggle Effects------------
    def toggleTableWidget(self):
        if self.mTable.isVisible():
            self.mTable.hide()
        else:
            self.mTable.show()

    def toggleButtonWidget(self):
        if self.mButton.isVisible():
            self.mButton.hide()
        else:
            self.mButton.show()

    def toggleVisionWidget(self):
        if self.mVision.isVisible():
            self.mVision.hide()
        else:
            self.mVision.show()

    def toggleLogWidget(self):
        if self.mLog.isVisible():
            self.mLog.hide()
        else:
            self.mLog.show()


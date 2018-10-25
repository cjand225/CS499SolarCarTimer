'''
Module: AppWindow.py
Purpose: Top level view object that handles most view information and talks with the controller to
         recieve data from modal

Depends On: PyQt5, Table.py, SemiAutoWidget.py,
'''

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi


from table.Table import Table
from table.SemiAutoWidget import SemiAutoWidget
from video.VisionWidget import VisionWidget
from log.LogWidget import LogWidget
from graph.GraphOptionsWidget import GraphOptions


class AppWindow(QMainWindow):

    def __init__(self):
        super(AppWindow, self).__init__()
        # initialize Window
        self.initMainWindow()

        # setup Menu Bar
        self.initMainMenu()

        # setup widgets

        self.initButtonWidget()
        self.initVisionWidget()
        self.initLogWidget()
        self.initTableWidget()
        self.initGraphWidget()

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

    #connects menubar submenus with menu handler functions
    def initMainMenu(self):
        self.menuFile.triggered[QAction].connect(self.handleFileMenu)
        self.menuEdit.triggered[QAction].connect(self.handleEditMenu)
        self.menuView.triggered[QAction].connect(self.handleViewMenu)
        self.menuHelp.triggered[QAction].connect(self.handleHelpMenu)


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
        #self.mGraph = Graph()

    #placeholder function
    def handleFileMenu(self, action):
        if action == self.actionNew:
            print("hi")
        if action == self.actionOpen:
            print("hi")
        if action == self.actionRecent:
            print("hi")
        if action == self.actionSave:
            print("hi")
        if action == self.actionSaveAs:
            print("hi")
        if action == self.actionClose:
            print("hi")
        if action == self.actionQuit:
            print("hi")

    # placeholder function
    def handleEditMenu(self, action):
        if action == self.actionUndo:
            print("hi")
        if action == self.actionRedo:
            print("hi")
        if action == self.actionCopy:
            print("hi")
        if action == self.actionCut:
            print("hi")
        if action == self.actionPaste:
            print("hi")
        if action == self.actionSelectRow:
            print("hi")
        if action == self.actionSelectColumn:
            print("hi")


    def handleViewMenu(self, action):
        if action == self.actionTable:
            self.toggleTableWidget()
        if action == self.actionLog:
            self.toggleLogWidget()
        if action == self.actionSemiAuto:
            self.toggleButtonWidget()
        if action == self.actionAuto:
            self.toggleVisionWidget()
        if action == self.actionGraphing:
            self.toggleGraphingWidget()

    # placeholder function
    def handleHelpMenu(self, action):
        if action == self.actionAbout:
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

    def toggleGraphingWidget(self):
        if self.mGraphOptions.isVisible():
            self.mGraphOptions.hide()
        else:
            self.mGraphOptions.show()


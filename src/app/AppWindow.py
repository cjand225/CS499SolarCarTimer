'''
Module: AppWindow.py
Purpose: Top level view object that handles most view information and talks with the controller to
         recieve data from modal

Depends On: PyQt5, TableView.py, SemiAutoWidget.py,
'''

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from src.table.Table import Table
from src.table.SemiAutoWidget import SemiAutoWidget
from src.video.VisionWidget import VisionWidget
from src.log.LogWidget import LogWidget
from src.graph.GraphOptionsWidget import GraphOptions


class AppWindow(QMainWindow):

    def __init__(self, uipath):
        super(AppWindow, self).__init__()
        # initialize Window
        self.UIPath = uipath

        #Widgets controlled by top view AppWindow
        self.VisionWidget = None
        self.TableWidget = None
        self.SemiAutoWidget = None
        self.GraphWidget = None
        self.GraphOptionsWidget = None
        self.LogWidget = None


        #declare initalizers here
        self.initMainWindow()
        self.initFileDialog()
        #self.connectComponents()


    def initMainWindow(self):
        self.mainWindowUI = loadUi(self.UIPath, self)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignHCenter,
                                            self.size(), QApplication.desktop().availableGeometry()))
        self.show()


    #def connectComponents(self):
        #view
        #self.actionTable.triggered.connect()
        #self.actionSemiAuto.triggered.connect()
        #self.actionAuto.triggered.connect()
        #self.actionLog.triggered.connect()
        #self.actionGraphing.triggered.connect()
        #help
        #self.actionAbout.triggered.connect()
        #self.actionHelp.triggered.connect()


    def addVison(self, vision):
        self.VisionWidget = vision

    def addTable(self, table):
        self.TableWidget = table

    def addSemiAuto(self, semiAuto):
        self.SemiAutoWidget = semiAuto

    def addGraph(self, graph):
        self.GraphWidget = graph

    def addGraphOptions(self, graphOps):
        self.GraphOptionsWidget = graphOps

    def addLog(self, log):
        self.LogWidget = log

    def initFileDialog(self):
        self.fileDialog = QFileDialog(self)

    def openFileDialog(self):
        fileName = self.fileDialog.getOpenFileName()
        if fileName:
            self.FileOpen = fileName
        else:
            self.FileOpen = None
        return fileName

    # TODO: set parameters for width/heigh/file formats - also add Save As part as well
    def saveAsFileDialog(self):
        fileName = self.fileDialog.getSaveFileName(self)
        if fileName:
            self.FileSave = fileName
        else:
            self.FileSave = None
        return fileName

    #TODO: set parameters for width/heigh/file formats
    def newFileDialog(self):
        fileName = self.fileDialog.getSaveFileName(self)
        return fileName


    #initalizes Closing Dialog for closeEvent overload
    def initCloseDialog(self, uipath):
        self.QuitMsg = QDialog()
        self.QuitMsg.ui = loadUi(uipath, self.QuitMsg)


    # Overloads closeEvent function to define what happens when main window X is clicked
    def closeEvent(self, a0: QCloseEvent):
         retval = self.QuitMsg.exec()  #grabs event code from Message box execution
         if retval == 1:    #if OK clicked - Close
             a0.accept()
             self.handleWidgetClosing()
         #if Cancel or MessageBox is closed - Ignore the signal
         if retval == 0:
             a0.ignore()


    #Makes sure all widgets if they exist close before closing mainwindow
    def handleWidgetClosing(self):
        if(self.TableWidget != None):
            self.TableWidget.close()
        if(self.VisionWidget != None):
            self.VisionWidget.close()
        if(self.LogWidget != None):
            self.LogWidget.close()
        if(self.GraphWidget != None):
            self.GraphWidget.close()
        self.close()



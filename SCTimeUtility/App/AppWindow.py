'''
    Module: AppWindow.py
    Purpose: A QMainWindow Object used and manipulated by the App class to control child widgets added
             from other modules as well as handle many of the signals created from gui elements.

    Depends On:
                Libs: PyQt5
                Classes: QWidget, QMainWindow, TableWidget, SemiAutoWidget, VisionWidget, GraphWidget,
                         LogWidget, GraphOptionsWidget

                Files: Table.py, SemiAutoWidget.py, VideoWidget.py, LogWidget.py, Graph.py
                       GraphWidget.py,
'''
import os
from pathlib import Path
from PyQt5.QtCore import QFile, QTextStream, Qt
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QDialog, QStyle
from PyQt5.uic import loadUi

from SCTimeUtility.Log.Log import getLog


class AppWindow(QMainWindow):

    def __init__(self, uipath):
        super(AppWindow, self).__init__()
        # initialize Window
        self.uiPath = uipath

        # Widgets controlled by top view AppWindow
        self.visionWidget = None
        self.tableWidget = None
        self.semiAutoWidget = None
        self.graphWidget = None
        self.logWidget = None
        self.leaderBoardWidget = None
        self.logger = getLog()
        self.aboutDialog = None
        self.helpDialog = None

        # declare initializers here
        self.initMainWindow()
        self.initFileDialog()

    ''' 

        Function: initMainWindow
        Parameters: N/A
        Return Value: N/A
        Purpose: Initializes the current class AppWindow as a QMainWindow, such that it loads the UI
                 and sets appropriate attributes and geometry.

    '''

    def initMainWindow(self):
        self.mainWindowUI = loadUi(self.uiPath, self)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignHCenter,
                                            self.size(), QApplication.desktop().availableGeometry()))
        # windows hack because for some undocumented reason anything aligned at the top of screen hides title bar.
        self.move(self.x(), self.y() - self.menuBar().y())
        self.show()

    ''' 

        Function: toggleWidget
        Parameters: widget, e
        Return Value: N/A
        Purpose: static method that involves toggling any of the widgets bound to the main App window, allowing
                 reduction of repetitious code for different widgets

    '''

    @staticmethod
    def toggleWidget(widget, e):
        if widget.isVisible():
            widget.hide()
        else:
            widget.show()

    ''' 

        Function: connectComponents()
        Parameters: self (QMainWindow)
        Return Value: N/A
        Purpose: Binds certain menu Actions to certain functions which involve toggling of particular
                children widgets. I.E. connect actionTable (View Menu Action) to tableWidget.toggle()

    '''

    def connectComponents(self):
        # File
        self.actionQuit.triggered.connect(self.handleWidgetClosing)

        # view
        if self.tableWidget is not None:
            self.actionTable.triggered.connect(lambda e: type(self).toggleWidget(self.tableWidget, e))
            self.pushTable.clicked.connect(lambda e: type(self).toggleWidget(self.tableWidget, e))

        if self.semiAutoWidget is not None:
            self.actionSemiAuto.triggered.connect(lambda e: type(self).toggleWidget(self.semiAutoWidget, e))
            self.pushSemiAuto.clicked.connect(lambda e: type(self).toggleWidget(self.semiAutoWidget, e))

        if self.visionWidget is not None:
            self.actionAuto.triggered.connect(lambda e: type(self).toggleWidget(self.visionWidget, e))
            self.pushVideo.clicked.connect(lambda e: type(self).toggleWidget(self.visionWidget, e))

        if self.logWidget is not None:
            self.actionLog.triggered.connect(lambda e: type(self).toggleWidget(self.logWidget, e))
            self.pushLogs.clicked.connect(lambda e: type(self).toggleWidget(self.logWidget, e))

        if self.graphWidget is not None:
            self.actionGraphing.triggered.connect(lambda e: type(self).toggleWidget(self.graphWidget, e))
            self.pushGraph.clicked.connect(lambda e: type(self).toggleWidget(self.graphWidget, e))

        if self.leaderBoardWidget is not None:
            self.actionLeaderBoard.triggered.connect(lambda e: type(self).toggleWidget(self.leaderBoardWidget, e))
            self.pushLeaderBoard.clicked.connect(lambda e: type(self).toggleWidget(self.leaderBoardWidget, e))

    ''' 
    
        Function: addVision
        Parameters: self, VisionWidget(QWidget)
        Return Value: N/A
        Purpose: Adds a VisionWidget from Vision Module, when called from App, which then is 
                 handled primarily by AppWindow and interfaces with the Table Module/User
    
    '''

    def addVision(self, vision):
        self.visionWidget = vision

    ''' 
    
        Function: addTable(self, Table)
        Parameters: self, Table(QTableView)
        Return Value: N/A
        Purpose: Adds a QWidget w/ QTableView from Table Module, when called from App, which is then
                 handled primarily by AppWindow and interfaced with the user.
    
    '''

    def addTable(self, table):
        self.tableWidget = table

    ''' 
    
        Function: addSemiAuto(self, semiAuto)
        Parameters:self, SemiAutoWidget(QWidget)
        Return Value: N/A
        Purpose: Adds a QWidget from Table Module, when function is invoked by App Class, which is then
                 handled primarily by AppWindow but bound to Storage through keybinds that interface with
                 the user.
    
    '''

    def addSemiAuto(self, semiAuto):
        self.semiAutoWidget = semiAuto

    ''' 
    
        Function: addGraph(self, Graph)
        Parameters: self, Graph(QWidget)
        Return Value: N/A
        Purpose: Adds a QWidget from Graphing Module, when function is invoked by App Class, which is then
                 handled primarily by AppWindow and interfaced with the User.
    
    '''

    def addGraph(self, graph):
        self.graphWidget = graph

    ''' 

        Function: addGraph(self, Graph)
        Parameters: self, Graph(QWidget)
        Return Value: N/A
        Purpose: Adds a QWidget from Graphing Module, when function is invoked by App Class, which is then
                 handled primarily by AppWindow and interfaced with the User.

    '''

    def addLeaderBoard(self, leaderboard):
        self.leaderBoardWidget = leaderboard

    ''' 
    
        Function: addLog(self, LogWidget)
        Parameters: self, logwid(QWidget)
        Return Value: N/A
        Purpose: Adds a QWidget from Logging Module, when function is invoked by App Class, which is then
                 handled primarily by AppWindow and Interfaced with the User through text updates within Widget.
    
    '''

    def addLog(self, pLogWidget):
        self.logWidget = pLogWidget

    ''' 
    
        Function: initFileDialog(self)
        Parameters: self
        Return Value: N/A
        Purpose: Initializes a QFileDialog used primarily for getting input from the user on where they 
                 would like to read or write a file. Needs to be called before openFileDialog, saveAsFileDialog,
                 and saveFileDialog
    
    '''

    def initFileDialog(self):
        self.fileDialog = QFileDialog(self)

    ''' 
    
        Function: openFileDialog(self)
        Parameters: self
        Return Value: fileName(String) or None
        Purpose: Opens a fileDialog to get input from the user on where the file they are
                 wanting to open happens to exist. if the file doesn't exist it'll return nothing,
                 otherwise it'll return the name of the file prepended with its directory.
    
    '''

    def openFileDialog(self):
        return self.fileDialog.getOpenFileName(self, 'Open File')

    '''
        Function: openDirDialog
        Parameters: self
        Return Value:
        Purpose: Returns a string value of the directory chosen, used for saving or opening a directory with multiple 
                 files located within.
    '''

    def openDirDialog(self):
        return self.fileDialog.getExistingDirectory(self, "Select Directory", str(Path.home()))

    ''' 
    
        Function: newFileDialog(self)
        Parameters: self
        Return Value: fileName(String)
        Purpose: Opens a FileDialog to recieve input from the user on where they would like to
                 save their new session. If nothing is pressed on return, it'll return None and
                 App will assume the default File Path for saving files, otherwise it'll return 
                 a filename with a prepended directory.
    
    '''

    def newFileDialog(self):
        return self.fileDialog.getSaveFileName(self, 'New File')

    ''' 
    
        Function: initCloseDialog(self, uiPAth)
        Parameters: self, uiPath(String)
        Return Value: N/A
        Purpose: Initializes a closing dialog for AppWindow, for use in overloading the close event
                 to protect user from accidental closing and/or losing unsaved work
    
    '''

    def initCloseDialog(self, uipath):
        self.QuitMsg = QDialog()
        self.QuitMsg.ui = loadUi(uipath, self.QuitMsg)

    ''' 
    
        Function: closeEvent(self, a0: QCloseEvent)
        Parameters: self, a0: QCloseEvent(QAction)
        Return Value: N/A
        Purpose: Overloads closeEvent Function for AppWindow(QMainWindow), such that it will
                 make sure the user actually intended on closing the program, as well as ensuring
                 its' children gui components have closed as well via handleWidgetClosing() called/
                 within handleClose() function
    
    '''

    def closeEvent(self, a0: QCloseEvent):
        retVal = self.QuitMsg.exec()  # grabs event code from Message box execution
        self.handleClose(retVal, a0)

    ''' 
    
        Function: handleWidgetClosing(self)
        Parameters: self
        Return Value: N/A
        Purpose: Function used to check if a widget exists and if it does, makes sure its close event is called
                 before calling the AppWindow close event.
    
    '''

    def handleWidgetClosing(self):
        if self.tableWidget is not None:
            self.tableWidget.close()
        if self.visionWidget is not None:
            self.visionWidget.close()
        if self.logWidget is not None:
            self.logWidget.close()
        if self.graphWidget is not None:
            self.graphWidget.close()
        if self.leaderBoardWidget is not None:
            self.leaderBoardWidget.close()
        if self.semiAutoWidget is not None:
            self.semiAutoWidget.close()
        self.close()

    '''
        Function: handleClose
        Parameters: self, Return Value, QCloseEven
        Return Value: N/A
        Purpose: Function that handles all closing based on user's choice of wanting to exit the program 
                 or not. 
    '''

    def handleClose(self, retVal, a0: QCloseEvent):
        if retVal == 1:  # if OK clicked - Close
            a0.accept()
            self.handleWidgetClosing()
        # if Cancel or MessageBox is closed - Ignore the signal
        if retVal == 0:
            a0.ignore()

    '''

        Function: createBrowserDialog
        Parameters: self, uiPath, filePath
        Return Value: return value of execution
        Purpose: Creates a general purpose brower dialog used to load any document from a file, mostly used for easy
                 streaming of manuals and other documention to the program itself.
    '''

    def createBrowserDialog(self, uiPath, filePath):
        # create and loadui for QDialog instance
        browserDialog = QDialog()
        browserDialog.ui = loadUi(uiPath, browserDialog)
        # if filePath is specified, create it, otherwise, return Rejected Enum
        if os.path.isfile(filePath):
            # open as a file stream
            file = QFile(filePath)
            file.open(QFile.ReadOnly | QFile.Text)
            stream = QTextStream(file)
            # direct stream as HTML, connect close button, execute and return value after close.
            browserDialog.ui.textBrowser.setHtml(stream.readAll())
            browserDialog.ui.buttonBox.clicked.connect(browserDialog.close)
            browserDialog.exec()
            # clean up after execution
            browserDialog.ui.buttonBox.clicked.disconnect()
            browserDialog.close()
            browserDialog.deleteLater()
            return QDialog.Accepted
        else:
            return QDialog.Rejected

    '''
        Function: createDecisionDialog
        Parameters: self, uiPath, filePath
        Return Value: QDialog.Accepted | QDialog.Rejected
        Purpose: Given paramaters, creates a decision based dialog i.e. yes or no, ok/cancel, to determine how to handle
                 next user interaction.
    '''

    def createDecisionDialog(self, uiPath, textField):
        pass

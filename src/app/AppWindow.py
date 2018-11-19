'''
Module: AppWindow.py
Purpose: A QMainWindow Object used and manipulated by the App class to control child widgets added
         from other modules as well as handle many of the signals created from gui elements.

Depends On:
            Libs: PyQt5
            Classes: QWidget, QMainWindow, TableWidget, SemiAutoWidget, VisionWidget, GraphWidget,
                     LogWidget, GraphOptionsWidget

            Files: Table.py, SemiAutoWidget.py, VisionWidget.py, LogWidget.py, GraphWidget.py
                   GraphOptions.py,
'''
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

import src.app.App
from src.table.AddCarDialog import AddCarDialog
from src.table.Car import Car
from src.video.Video import Video


# from src.cloud.GoogleDriveBrowser import GoogleDriveBrowser


class AppWindow(QMainWindow):

    def __init__(self, uipath):
        super(AppWindow, self).__init__()
        # initialize Window
        self.UIPath = uipath

        # Widgets controlled by top view AppWindow
        self.VisionWidget = None
        self.TableWidget = None
        self.SemiAutoWidget = None
        self.GraphWidget = None
        self.GraphOptionsWidget = None
        self.LogWidget = None
        self.LeaderBoardWidget = None

        # declare initalizers here
        self.initMainWindow()
        self.initFileDialog()
        self.connectComponents()

    ''' 

        Function: initMainWindow
        Parameters: N/A
        Return Value: N/A
        Purpose: Initializes the current class AppWindow as a QMainWindow, such that it loads the UI
                 and sets appropriate attributes and geometry.

    '''

    def initMainWindow(self):
        self.mainWindowUI = loadUi(self.UIPath, self)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignHCenter,
                                            self.size(), QApplication.desktop().availableGeometry()))
        self.show()


    ''' 

        Function: toggleWidget
        Parameters: widget, e
        Return Value: N/A
        Purpose: static method that involves toggling any of the widgets bound to the main app window, allowing
                 reduction of repitious code for different widgets

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
        # view
        self.actionTable.triggered.connect(lambda e: type(self).toggleWidget(self.TableWidget, e))
        self.actionSemiAuto.triggered.connect(lambda e: type(self).toggleWidget(self.SemiAutoWidget, e))
        self.actionAuto.triggered.connect(lambda e: type(self).toggleWidget(self.VisionWidget, e))
        #self.actionLog.triggered.connect(lambda e: type(self).toggleWidget(self.LogWidget, e))
        #self.actionGraphing.triggered.connect(lambda e: type(self).toggleWidget(self.GraphWidget), e)
        #self.actionLeaderBoard.triggered.connect(lambda e: type(self).toggleWidget(self.LeaderBoardWidget, e))

        #Center Widget
        self.pushTable.clicked.connect(lambda e: type(self).toggleWidget(self.TableWidget, e))
        self.pushSemiAuto.clicked.connect(lambda e: type(self).toggleWidget(self.SemiAutoWidget, e))
        self.pushVideo.clicked.connect(lambda e: type(self).toggleWidget(self.VisionWidget, e))
        self.pushLeaderBoard.clicked.connect(lambda e: type(self).toggleWidget(self.LeaderBoardWidget, e))
        self.pushGraph.clicked.connect(lambda e: type(self).toggleWidget(self.GraphWidget, e))
        self.pushLogs.clicked.connect(lambda e: type(self).toggleWidget(self.LogWidget, e))

        # help
        self.actionAbout.triggered.connect(self.handleAboutDialog)
        self.actionHelp.triggered.connect(self.handleHelpDialog)

    ''' 
    
        Function: addVision
        Parameters: self, VisionWidget(QWidget)
        Return Value: N/A
        Purpose: Adds a VisionWidget from Vision Module, when called from App, which then is 
                 handled primarily by AppWindow and interfaces with the Table Module/User
    
    '''

    def addVision(self, vision):
        self.VisionWidget = vision

    ''' 
    
        Function: addTable(self, table)
        Parameters: self, table(QTableView)
        Return Value: N/A
        Purpose: Adds a QWidget w/ QTableView from Table Module, when called from App, which is then
                 handled primarily by AppWindow and interfaced with the user.
    
    '''

    def addTable(self, table):
        self.TableWidget = table

    ''' 
    
        Function: addSemiAuto(self, semiAuto)
        Parameters:self, SemiAutoWidget(QWidget)
        Return Value: N/A
        Purpose: Adds a QWidget from Table Module, when function is invoked by App Class, which is then
                 handled primarily by AppWindow but bound to Storage through keybinds that interface with
                 the user.
    
    '''

    def addSemiAuto(self, semiAuto):
        self.SemiAutoWidget = semiAuto

    ''' 
    
        Function: addGraph(self, graph)
        Parameters: self, Graph(QWidget)
        Return Value: N/A
        Purpose: Adds a QWidget from Graphing Module, when function is invoked by App Class, which is then
                 handled primarily by AppWindow and interfaced with the User.
    
    '''

    def addGraph(self, graph):
        self.GraphWidget = graph

    ''' 

        Function: addGraph(self, graph)
        Parameters: self, Graph(QWidget)
        Return Value: N/A
        Purpose: Adds a QWidget from Graphing Module, when function is invoked by App Class, which is then
                 handled primarily by AppWindow and interfaced with the User.

    '''

    def addLeaderBoard(self, leaderboard):
        self.LeaderBoardWidget = leaderboard

    ''' 
    
        Function: addLog(self, LogWidget)
        Parameters: self, logwid(QWidget)
        Return Value: N/A
        Purpose: Adds a QWidget from Logging Module, when function is invoked by App Class, which is then
                 handled primarily by AppWindow and Interfaced with the User through text updates within Widget.
    
    '''

    def addLog(self, logwid):
        self.LogWidget = logwid

    ''' 
    
        Function: initFileDialog(self)
        Parameters: self
        Return Value: N/A
        Purpose: Initalizes a QFileDialog used primarily for getting input from the user on where they 
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
        fileName = self.fileDialog.getOpenFileName()
        if fileName:
            return fileName[0]
        else:
            return None

    ''' 
        Function: saveAsFileDialog(self)
        Parameters: self
        Return Value: FileName(String) or None
        Purpose: Opens a fileDialog to get input from the user on where they would like to save
                 their current session to. If Nothing is pressed on return, it'll return None,
                 otherwise it'll return the name and place of where they would like to save their
                 file.
    '''

    # TODO: set parameters for width/heigh/file formats - also add Save As part as well
    def saveAsFileDialog(self):
        fileName = self.fileDialog.getSaveFileName(self)
        if fileName:
            return fileName[0]
        else:
            return None
        # return fileName[0]

    ''' 
    
        Function: newFileDialog(self)
        Parameters: self
        Return Value: fileName(String)
        Purpose: Opens a FileDialog to recieve input from the user on where they would like to
                 save their new session. If nothing is pressed on return, it'll return None and
                 App will assume the default File Path for saving files, otherwise it'll return 
                 a filename with a prepended directory.
    
    '''

    # TODO: set parameters for width/heigh/file formats
    def newFileDialog(self):
        fileName = self.fileDialog.getSaveFileName(self)
        return fileName

    ''' 
    
        Function: initCloseDialog(self, uiPAth)
        Parameters: self, uiPath(String)
        Return Value: N/A
        Purpose: Initalizes a closing dialog for AppWindow, for use in overloading the close event
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
                 its' children gui components have closed as well via handleWidgetClosing()
    
    '''

    def closeEvent(self, a0: QCloseEvent):
        retval = self.QuitMsg.exec()  # grabs event code from Message box execution
        if retval == 1:  # if OK clicked - Close
            a0.accept()
            self.handleWidgetClosing()
        # if Cancel or MessageBox is closed - Ignore the signal
        if retval == 0:
            a0.ignore()

    ''' 
    
        Function: handleWidgetClosing(self)
        Parameters: self
        Return Value: N/A
        Purpose: Function used to check if a widget exists and if it does, makes sure its close event is called
                 before calling the AppWindow close event.
    
    '''
    def handleWidgetClosing(self):
        if (self.TableWidget != None):
            self.TableWidget.close()
        if (self.VisionWidget != None):
            self.VisionWidget.close()
        if (self.LogWidget != None):
            self.LogWidget.close()
        if (self.GraphWidget != None):
            self.GraphWidget.close()
        if (self.LeaderBoardWidget != None):
            self.LeaderBoardWidget.close()
        if(self.SemiAutoWidget != None):
            self.SemiAutoWidget.close()
        self.close()


    '''

        Function: initHelpDialog
        Parameters: uiPath, filePath
        Return Value: N/A
        Purpose: Instances a QDialog given a filepath in UIpath parameter and a file containing data to display
                 given by filePath, loads file into a text stream that then is set as html for the textbrowser
                 built into the Dialog's ui file. If no file path is given, it'll just return none


    '''
    def initHelpDialog(self, uiPath, filePath=None):
        self.HelpDialog = QDialog()
        self.HelpDialog.ui = loadUi(uiPath, self.HelpDialog)
        if(filePath != None):
            file = QFile(filePath)
            file.open(QFile.ReadOnly | QFile.Text)
            stream = QTextStream(file)
            self.HelpDialog.ui.textBrowser.setHtml(stream.readAll())

    '''

        Function: initAboutDialog
        Parameters: uiPath, filePath
        Return Value: N/A
        Purpose: Instances a QDialog given a filepath in UIpath parameter and a file containing data to display
                 given by filePath, loads file into a text stream that then is set as html for the textbrowser
                 built into the Dialog's ui file. If no file path is given, it'll just return none 

    '''
    def initAboutDialog(self, uiPath, filePath=None):
        self.AboutDialog = QDialog()
        self.AboutDialog.ui = loadUi(uiPath, self.AboutDialog)
        if filePath != None:
            file = QFile(filePath)
            file.open(QFile.ReadOnly | QFile.Text)
            stream = QTextStream(file)
            self.AboutDialog.ui.textBrowser.setHtml(stream.readAll())

    '''

        Function: handleAboutDialog
        Parameters: self
        Return Value: N/A
        Purpose: Binds the buttonbox to the close event allowing the ok/close buttons to close the dialog
                 and then executes the dialog to display out to the user.


    '''
    def handleAboutDialog(self):
        self.AboutDialog.ui.buttonBox.clicked.connect(self.AboutDialog.close)
        self.AboutDialog.exec()



    '''
        
        Function: handleHelpDialog
        Parameters: self
        Return Value: N/A
        Purpose: Binds the buttonbox to the close event allowing the ok/close buttons to close the dialog
                 and then executes the dialog to display out to the user.
    
    
    '''
    def handleHelpDialog(self):
        self.HelpDialog.ui.buttonBox.clicked.connect(self.HelpDialog.close)
        self.HelpDialog.exec()




    def addCarDialog(self):
        carDialog = AddCarDialog(src.app.App.App.addCarDialogUIPath)
        retVal = carDialog.exec()
        if retVal == QDialog.Accepted:
            carNumber = int(carDialog.carNumber)
            return Car(0, carDialog.teamName, carNumber)
        else:
            return None

    # def googleDriveDialog(self):
    #     driveDialog = GoogleDriveBrowser(src.app.App.App.googleDriveUIPath)
    #     retVal = driveDialog.exec()

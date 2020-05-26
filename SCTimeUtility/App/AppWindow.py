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

from SCTimeUtility.Log.Log import get_log


class AppWindow(QMainWindow):

    def __init__(self, resource_path):
        super(AppWindow, self).__init__()
        # initialize Window
        self.resource_path = resource_path
        self.logger = get_log()

        # Widgets controlled by top view AppWindow
        self.vision_widget = None
        self.table_widget = None
        self.semi_auto_widget = None
        self.graph_widget = None
        self.log_widget = None
        self.leaderboard_widget = None
        self.about_dialog = None
        self.help_dialog = None

        # declare initializations here
        self.init_widget()
        self.init_file_dialog()

    ''' 

        Function: initMainWindow
        Parameters: N/A
        Return Value: N/A
        Purpose: Initializes the current class AppWindow as a QMainWindow, such that it loads the UI
                 and sets appropriate attributes and geometry.

    '''

    def init_widget(self):
        self.widget = loadUi(self.resource_path, self)
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
    def toggle_widget(widget, e):
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

    def bind_components(self):
        # File
        self.action_quit.triggered.connect(self.widget_close_event)

        # view
        if self.table_widget is not None:
            self.action_table.triggered.connect(lambda e: type(self).toggle_widget(self.table_widget, e))
            self.table_pb.clicked.connect(lambda e: type(self).toggle_widget(self.table_widget, e))

        if self.semi_auto_widget is not None:
            self.action_semi_auto.triggered.connect(lambda e: type(self).toggle_widget(self.semi_auto_widget, e))
            self.semi_auto_pb.clicked.connect(lambda e: type(self).toggle_widget(self.semi_auto_widget, e))

        if self.vision_widget is not None:
            self.action_auto.triggered.connect(lambda e: type(self).toggle_widget(self.vision_widget, e))
            self.vision_pb.clicked.connect(lambda e: type(self).toggle_widget(self.vision_widget, e))

        if self.log_widget is not None:
            self.action_log.triggered.connect(lambda e: type(self).toggle_widget(self.log_widget, e))
            self.log_pb.clicked.connect(lambda e: type(self).toggle_widget(self.log_widget, e))

        if self.graph_widget is not None:
            self.action_graph.triggered.connect(lambda e: type(self).toggle_widget(self.graph_widget, e))
            self.graph_pb.clicked.connect(lambda e: type(self).toggle_widget(self.graph_widget, e))

        if self.leaderboard_widget is not None:
            self.action_leaderboard.triggered.connect(lambda e: type(self).toggle_widget(self.leaderboard_widget, e))
            self.leaderboard_pb.clicked.connect(lambda e: type(self).toggle_widget(self.leaderboard_widget, e))

    ''' 
    
        Function: addVision
        Parameters: self, VisionWidget(QWidget)
        Return Value: N/A
        Purpose: Adds a VisionWidget from Vision Module, when called from App, which then is 
                 handled primarily by AppWindow and interfaces with the Table Module/User
    
    '''

    def add_vision(self, vision):
        self.vision_widget = vision

    ''' 
    
        Function: addTable(self, Table)
        Parameters: self, Table(QTableView)
        Return Value: N/A
        Purpose: Adds a QWidget w/ QTableView from Table Module, when called from App, which is then
                 handled primarily by AppWindow and interfaced with the user.
    
    '''

    def add_table(self, table):
        self.table_widget = table

    ''' 
    
        Function: addSemiAuto(self, semiAuto)
        Parameters:self, SemiAutoWidget(QWidget)
        Return Value: N/A
        Purpose: Adds a QWidget from Table Module, when function is invoked by App Class, which is then
                 handled primarily by AppWindow but bound to Storage through keybinds that interface with
                 the user.
    
    '''

    def add_semi_auto(self, semiAuto):
        self.semi_auto_widget = semiAuto

    ''' 
    
        Function: addGraph(self, Graph)
        Parameters: self, Graph(QWidget)
        Return Value: N/A
        Purpose: Adds a QWidget from Graphing Module, when function is invoked by App Class, which is then
                 handled primarily by AppWindow and interfaced with the User.
    
    '''

    def add_graph(self, graph):
        self.graph_widget = graph

    ''' 

        Function: addGraph(self, Graph)
        Parameters: self, Graph(QWidget)
        Return Value: N/A
        Purpose: Adds a QWidget from Graphing Module, when function is invoked by App Class, which is then
                 handled primarily by AppWindow and interfaced with the User.

    '''

    def add_leaderboard(self, leaderboard):
        self.leaderboard_widget = leaderboard

    ''' 
    
        Function: addLog(self, LogWidget)
        Parameters: self, logwid(QWidget)
        Return Value: N/A
        Purpose: Adds a QWidget from Logging Module, when function is invoked by App Class, which is then
                 handled primarily by AppWindow and Interfaced with the User through text updates within Widget.
    
    '''

    def add_log(self, pLogWidget):
        self.log_widget = pLogWidget

    ''' 
    
        Function: initFileDialog(self)
        Parameters: self
        Return Value: N/A
        Purpose: Initializes a QFileDialog used primarily for getting input from the user on where they 
                 would like to read or write a file. Needs to be called before openFileDialog, saveAsFileDialog,
                 and saveFileDialog
    
    '''

    def init_file_dialog(self):
        self.file_dialog = QFileDialog(self)

    ''' 
    
        Function: openFileDialog(self)
        Parameters: self
        Return Value: fileName(String) or None
        Purpose: Opens a fileDialog to get input from the user on where the file they are
                 wanting to open happens to exist. if the file doesn't exist it'll return nothing,
                 otherwise it'll return the name of the file prepended with its directory.
    
    '''

    def open_file_dialog(self):
        return self.file_dialog.getOpenFileName(self, 'Open File')

    '''
        Function: openDirDialog
        Parameters: self
        Return Value:
        Purpose: Returns a string value of the directory chosen, used for saving or opening a directory with multiple 
                 files located within.
    '''

    def open_directory_dialog(self):
        return self.file_dialog.getExistingDirectory(self, "Select Directory", str(Path.home()))

    ''' 
    
        Function: newFileDialog(self)
        Parameters: self
        Return Value: fileName(String)
        Purpose: Opens a FileDialog to recieve input from the user on where they would like to
                 save their new session. If nothing is pressed on return, it'll return None and
                 App will assume the default File Path for saving files, otherwise it'll return 
                 a filename with a prepended directory.
    
    '''

    def new_file_dialog(self):
        return self.file_dialog.getSaveFileName(self, 'New File')

    ''' 
    
        Function: initCloseDialog(self, uiPAth)
        Parameters: self, uiPath(String)
        Return Value: N/A
        Purpose: Initializes a closing dialog for AppWindow, for use in overloading the close event
                 to protect user from accidental closing and/or losing unsaved work
    
    '''

    def init_close_dialog(self, resource_path):
        self.quit_message_dialog = QDialog()
        self.quit_message_dialog.ui = loadUi(resource_path, self.quit_message_dialog)

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
        ret_val = self.quit_message_dialog.exec()  # grabs event code from Message box execution
        self.handleClose(ret_val, a0)

    ''' 
    
        Function: handleWidgetClosing(self)
        Parameters: self
        Return Value: N/A
        Purpose: Function used to check if a widget exists and if it does, makes sure its close event is called
                 before calling the AppWindow close event.
    
    '''

    def widget_close_event(self):
        if self.table_widget is not None:
            self.table_widget.close()
        if self.vision_widget is not None:
            self.vision_widget.close()
        if self.log_widget is not None:
            self.log_widget.close()
        if self.graph_widget is not None:
            self.graph_widget.close()
        if self.leaderboard_widget is not None:
            self.leaderboard_widget.close()
        if self.semi_auto_widget is not None:
            self.semi_auto_widget.close()
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
            self.widget_close_event()
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

    def create_browser_dialog(self, resource_path, file_path):
        browser_dialog = QDialog()
        browser_dialog.ui = loadUi(resource_path, browser_dialog)
        if os.path.isfile(file_path):
            file = QFile(file_path)
            file.open(QFile.ReadOnly | QFile.Text)
            stream = QTextStream(file)
            browser_dialog.ui.textBrowser.setHtml(stream.readAll())
            browser_dialog.ui.buttonBox.clicked.connect(browser_dialog.close)
            browser_dialog.exec()
            browser_dialog.ui.buttonBox.clicked.disconnect()
            browser_dialog.close()
            browser_dialog.deleteLater()
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

    def create_decision_dialog(self, uiPath, textField):
        pass

'''
Module: App.py
Purpose: Controller for entire application, used to periodically update project with data to and from the
         modal.

'''

import os
import sys

from PyQt5.Qt import *

from src.graph.GraphWidget import Graph
from src.app.AppWindow import AppWindow
from src.system.IO import loadCSV, saveCSV
from src.table.CarStorage import CarStorage
from src.table.SemiAutoWidget import SemiAutoWidget
from src.table.Table import Table
from src.video.Video import Video
from src.log.LogWidget import LogWidget

from src.log.Log import getLogger, createLogger


class App():
    resourcesDir = os.path.abspath(os.path.join(__file__, "./../../../resources"))
    manualDir = os.path.abspath(os.path.join(__file__, "./../../../manuals"))

    mainUIPath = os.path.join(resourcesDir, 'AppWindow.ui')
    tableUIPath = os.path.join(resourcesDir, 'TableView.ui')
    visionUIPath = os.path.join(resourcesDir, 'Video.ui')
    logUIPath = os.path.join(resourcesDir, 'Log.ui')
    semiAutoUIPath = os.path.join(resourcesDir, 'SemiAuto.ui')
    quitDialogUIPath = os.path.join(resourcesDir, 'QuitDialog.ui')
    addCarDialogUIPath = os.path.join(resourcesDir, 'addCarDialog.ui')
    # googleDriveUIPath = os.path.join(resourcesDir,'GoogleDriveView.ui')
    helpDialogUIPath = os.path.join(resourcesDir, 'HelpDialog.ui')
    aboutDialogUIPath = os.path.join(resourcesDir, 'AboutDialog.ui')
    GraphUIPath = os.path.join(resourcesDir, 'GraphOptions.ui')
    userManPath = os.path.join(manualDir, 'USER_MANUAL.html')
    aboutPath = os.path.join(manualDir, 'about.html')

    def __init__(self):
        self.Application = None
        self.mainWindow = None
        self.running = False

        # creating Logger
        createLogger()

        # read/write paths
        self.defaultSavePath = ''

        # Forward Module Declaration
        self.log = getLogger()

        self.tableView = None
        self.SemiAuto = None
        self.Vision = None
        self.graph = None
        self.logWidget = None
        self.leaderBoard = None

        # read/write files
        self.writeFile = None
        self.readFile = None

        # Initializing everything
        self.initApplication()
        self.initMainWindow()
        self.initLog()
        self.initTableView()
        self.initSemiAuto()
        self.initVision()
        self.initGraph()
        self.initLeaderBoard()

        # adding and connecting essential components to user interface
        self.addComponents()
        self.connectActionsMainWindow()

    def semiAutoStart(self, car, semiAutoIndex, startTime):
        self.tableView.CarStoreList.storageList[car.ID].initialTime = startTime

    def semiAutoRecord(self, car, semiAutoIndex, recordedTime):
        if self.tableView.CarStoreList.storageList[car.ID].LapList:
            elapsedTime = recordedTime - self.tableView.CarStoreList.storageList[car.ID].LapList[-1].recordedTime
        else:
            elapsedTime = recordedTime - car.initialTime
        self.tableView.CarStoreList.appendLapTime(car.ID, elapsedTime)

    def tableClickEvent(self, i):
        if i.column() == len(self.tableView.CarStoreList.storageList):
            self.addCar()

    ''' 

        Function: initApplication(self)
        Parameters: self
        Return Value: N/A
        Purpose: Initializes the QApplication, required for running and maintaing program.

    '''

    def initApplication(self):
        self.Application = QApplication(sys.argv)

    ''' 

        Function: initMainWindow(self)
        Parameters: self
        Return Value: N/A
        Purpose: Initializes AppWindow in the mainWindow Variable attatched to App Class as well as
                 Initalizing any functions related to the AppWindow Class

    '''

    def initMainWindow(self):
        self.mainWindow = AppWindow(type(self).mainUIPath)
        self.mainWindow.initCloseDialog(type(self).quitDialogUIPath)
        self.mainWindow.initHelpDialog(type(self).helpDialogUIPath, type(self).userManPath)
        self.mainWindow.initAboutDialog(type(self).aboutDialogUIPath, type(self).aboutPath)

    ''' 

        Function: initTableview(self)
        Parameters: self
        Return Value: N/A
        Purpose: Initializes the Table Class (w/ a path to the view's UI), that is its own controller for handling 
                 both its internal model and View class (however view class is passed to AppWindow to handle afterwards)

    '''

    def initTableView(self):
        self.tableView = Table(type(self).tableUIPath)
        self.tableView.tableView.doubleClicked.connect(self.tableClickEvent)
        self.log.debug('[' + __name__ + ']' + ' Table Initialized')

    '''
    
        Function: initSemiAuto(self)
        Parameters: self
        Return Value: N/A
        Purpose: Initializes the Semi Auto class (w/ path to view's UI) that is its own controller for handling
                 semi-automatic recording times for the table.
    
    '''

    def initSemiAuto(self):
        self.SemiAuto = SemiAutoWidget(type(self).semiAutoUIPath)
        self.log.debug('[' + __name__ + '] ' + 'Semi-Auto Initialized')

    ''' 

        Function: initVision(self)
        Parameters: self
        Return Value: N/A
        Purpose: Initializes the Vision Class (w/ a path to the View's UI), that handled camera interfacing, image
                 processing, and OCR related tasks, which then can interface with the Table Class in order to update
                 Various Cars with Laptime Information

    '''

    def initVision(self):
        self.Vision = Video(self.visionUIPath)
        self.log.debug('[' + __name__ + '] ' + 'Video Initialized')

    ''' 

        Function: initLog(self)
        Parameters: self
        Return Value: N/A
        Purpose: Initializes the Log Class (w/ a path to the View's UI and Writing directory), that handles
                 file writes to a specified file when the Log Class is invoked.

    '''

    def initLog(self):
        self.logWidget = LogWidget(self.logUIPath)
        if self.logWidget is not None:
            self.log.debug('[' + __name__ + '] ' + 'Log module initialized')
        else:
            self.log.debug('[' + __name__ + '] ' + 'Log module failed to initialize')

    ''' 

        Function: initGraph(self)
        Parameters: self
        Return Value: N/A
        Purpose: initializes the Graphing Module (w/ a path to the View's UI), which then when given information
                 in the form of lists and user specified information, can create Graphs via its own VieW

    '''

    def initGraph(self):
        self.graph = Graph(self.GraphUIPath)
        if self.graph is not None:
            self.log.debug('[' + __name__ + '] ' + 'Graph module initialized')
        else:
            self.log.debug('[' + __name__ + '] ' + 'Graph module failed to initialize')

    ''' 

        Function: initLeaderBoard(self)
        Parameters: self
        Return Value: N/A
        Purpose: initializes the LeaderBoard Module (w/ a path to the View's UI), which then when given information
                 in the form of lists of information based on racing data can create a visual list from its view for user.

    '''

    def initLeaderBoard(self):
        self.leaderBoard = None
        if self.leaderBoard is not None:
            self.log.debug('[' + __name__ + '] ' + 'LeaderBoard module initialized')
        else:
            self.log.debug('[' + __name__ + '] ' + 'LeaderBoard module failed to initialize')

    ''' 

        Function: addComponents(self)
        Parameters: self
        Return Value: N/A
        Purpose: Adds widgets from each module to mainWindow(AppWindow) to be handled as a sub component
                 of the overall View of the program.

    '''

    def addComponents(self):
        self.log.debug('[' + __name__ + '] ' + 'Adding components to Main Window')

        if self.logWidget is not None:
            self.mainWindow.addLog(self.logWidget)
        if self.tableView is not None:
            self.mainWindow.addTable(self.tableView.getTableWidget())
        if self.SemiAuto is not None:
            self.mainWindow.addSemiAuto(self.SemiAuto)
        if self.Vision is not None:
            self.mainWindow.addVision(self.Vision.getWidget())
        if self.graph is not None:
            self.mainWindow.addGraph(self.graph)
        if self.leaderBoard is not None:
            self.mainWindow.addLeaderBoard(self.leaderBoard.getWidget())

        self.mainWindow.connectComponents()

    ''' 

        Function: connectActionsMainWindow(self)
        Parameters: self
        Return Value: N/A
        Purpose: connects Actions relating to the QMainWindow(AppWindow) that require a higher level scope
                 than what is normally allowed to AppWindow such as newfile, openfile, savefile, saveAs.

    '''

    def connectActionsMainWindow(self):
        # FileMenu
        self.mainWindow.actionNew.triggered.connect(self.newFile)
        self.mainWindow.actionOpen.triggered.connect(self.openFile)
        self.mainWindow.actionSave.triggered.connect(self.saveFile)
        self.mainWindow.actionSaveAs.triggered.connect(self.saveAsFile)
        # self.mainWindow.actionUpload.triggered.connect(self.upload)

        # self.mainWindow.SemiAutoWidget.startClicked.connect(self.semiAutoStart)
        # self.mainWindow.SemiAutoWidget.carRecord.connect(self.semiAutoRecord)
        # self.mainWindow.saveShortcut.activated.connect(self.saveFile)
        self.tableView.saveShortcut.activated.connect(self.saveFile)

        # Edit Menu
        self.mainWindow.actionAddCar.triggered.connect(self.addCar)

        # Help Menu

    ''' 
    
        Function: run(self)
        Parameters: self
        Return Value: N/A
        Purpose: Runs entire Program until Application returns from executing, which then closes with a 
                 proper exit code.

    '''

    def run(self):
        self.running = True
        sys.exit(self.Application.exec_())

    ''' 

        Function: saveFile(self)
        Parameters: self
        Return Value: N/A
        Purpose: Saves the current session of data from Table Model to the currently chosen writeFile,
                 if the file happens to not exist, the writeFile file will then ask the user to name such
                 a file to be created.

    '''

    def saveFile(self):
        if self.writeFile is not None and self.writeFile != '':
            saveCSV(self.tableView.CarStoreList, self.writeFile)
            self.log.debug('[' + __name__ + '] ' + 'Data saved to: ' + self.writeFile)
        else:
            self.log.debug('[' + __name__ + '] ' + 'No Write file currently found, requesting new one.')
            self.saveAsFile()

        # else use writeFile

        # continue to dump save file

    ''' 

        Function: SaveAsFile(self)
        Parameters: self
        Return Value: N/A
        Purpose: Saves the current session of data from TableModel to the writeFile chosen by the user,
                 if the user doesn't choose a filename, it'll assume a default file name to save as under
                 the current working directory.

    '''

    def saveAsFile(self):
        newFile = self.mainWindow.saveAsFileDialog()
        if newFile is not None and newFile != '':
            # write file to location
            self.writeFile = newFile
            self.saveFile()
            self.log.debug('[' + __name__ + '] ' + 'Data saved to: ' + self.writeFile)
        else:
            self.log.debug('[' + __name__ + '] ' + 'Could not save data to: ' + newFile)

    ''' 

        Function: openFile(self)
        Parameters: self
        Return Value: N/A
        Purpose: opens a file chosen by the user via FileDialog that is then opened and read/parsed
                 into the Table Model

    '''

    def openFile(self):
        readFile = self.mainWindow.openFileDialog()
        if readFile:
            self.writeFile = readFile
            cars = loadCSV(readFile)
            self.mainWindow.SemiAutoWidget.deleteAllCars()
            self.tableView.CarStoreList = CarStorage()
            self.tableView.initTableModel()
            self.tableView.tableView.setModel(self.tableView.TableMod)
            for car in cars:
                self.addCar(car)

    ''' 

        Function: newFile(self)
        Parameters: self
        Return Value: N/A
        Purpose: Clears any currently existing tableModel, prompts user to set a filename via FileDialog,
                 then saves that as the current writeFile to be used for anything further.

    '''

    def newFile(self):
        self.writeFile = self.mainWindow.saveAsFileDialog()
        if self.writeFile is not None and self.writeFile != '':
            self.log.debug('[' + __name__ + '] ' + 'Data saved to new file: ' + self.writeFile)
        else:
            self.log.debug('[' + __name__ + '] ' + 'Failed to create new file (bad path given)')

    def addCar(self, newCar=None):
        if not newCar:
            newCar = self.mainWindow.addCarDialog()
            if newCar:
                newCar.ID = len(self.tableView.CarStoreList.storageList)
        if newCar:
            self.tableView.CarStoreList.addExistingCar(newCar)
            self.mainWindow.SemiAutoWidget.addCar(newCar)
            self.graph.addCar(newCar)

    # def upload(self):
    #     self.mainWindow.googleDriveDialog()

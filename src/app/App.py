'''
Module: App.py
Purpose: Controller for entire application, used to periodically update project with data to and from the
         modal.

'''

import os, sys
from PyQt5.QtCore import *
from PyQt5.Qt import *
from src.app.AppWindow import AppWindow
from src.table.Table import Table
from src.table.SemiAutoWidget import SemiAutoWidget



class App():
    resourcesDir = os.path.abspath(os.path.join(__file__,"./../../../resources"))
    mainUIPath = os.path.join(resourcesDir,'App.ui')
    tableUIPath = os.path.join(resourcesDir,'Table.ui')
    visionUIPath = os.path.join(resourcesDir,'Video.ui')
    logUIPath = os.path.join(resourcesDir,'Log.ui')
    semiAutoUIPath = os.path.join(resourcesDir,'Buttons.ui')
    quitDialogUIPath = os.path.join(resourcesDir,'QuitDialog.ui')
    addCarDialogUIPath = os.path.join(resourcesDir,'addCarDialog.ui')
    # googleDriveUIPath = os.path.join(resourcesDir,'GoogleDriveView.ui')
    LogPath = os.path.abspath(os.path.join(__file__, '../../logs/'))
    
    def __init__(self):
        self.Application = None
        self.mainWindow = None
        self.running = False

        #read/write paths
        self.defaultSavePath = ''

        self.vision = None
        self.tableView = None

        #read/write files
        self.writeFile = None
        self.readFile = None

        self.initApplication()
        self.initMainWindow()
        self.initTableView()
        #self.initVision()
        #self.initLog()
        #self.initGraph()

        self.addComponents()
        self.connectActionsMainWindow()
        self.mainWindow.SemiAutoWidget.startClicked.connect(self.semiAutoStart)
        self.mainWindow.SemiAutoWidget.carRecord.connect(self.semiAutoRecord)

    def semiAutoStart(self,car,semiAutoIndex,startTime):
        self.tableView.CarStoreList.storageList[car.ID].initialTime = startTime

    def semiAutoRecord(self,car,semiAutoIndex,recordedTime):
        if self.tableView.CarStoreList.storageList[car.ID].LapList:
            elapsedTime = recordedTime - self.tableView.CarStoreList.storageList[car.ID].LapList[-1].recordedTime
        else:
            elapsedTime = recordedTime - car.initialTime
        self.tableView.CarStoreList.appendLapTime(car.ID,elapsedTime)

    @staticmethod
    def toggleWidget(widget,e):
        if widget.isVisible():
            widget.hide()
        else:
            widget.show()


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

    ''' 

        Function: initTableview(self)
        Parameters: self
        Return Value: N/A
        Purpose: Initializes the Table Class (w/ a path to the view's UI), that is its own controller for handling 
                 both its internal model and View class (however view class is passed to AppWindow to handle afterwards)

    '''
    def initTableView(self):
        self.tableView = Table(type(self).tableUIPath)

    ''' 

        Function: initVision(self)
        Parameters: self
        Return Value: N/A
        Purpose: Initalizes the Vision Class (w/ a path to the View's UI), that handled camera interfacing, image
                 processing, and OCR related tasks, which then can interface with the Table Class in order to update
                 Various Cars with Laptime Information

    '''
    def initVision(self):
        self.vision = None


    ''' 

        Function: initLog(self)
        Parameters: self
        Return Value: N/A
        Purpose: Initializes the Log Class (w/ a path to the View's UI and Writing directory), that handles
                 file writes to a specified file when the Log Class is invoked.

    '''
    def initLog(self):
        self.log = None

    ''' 

        Function: initGraph(self)
        Parameters: self
        Return Value: N/A
        Purpose: initializes the Graphing Module (w/ a path to the View's UI), which then when given information
                 in the form of lists and user specified information, can create Graphs via its own VieW

    '''
    def initGraph(self):
        self.graph = None

    ''' 

        Function: addComponents(self)
        Parameters: self
        Return Value: N/A
        Purpose: Adds widgets from each module to mainWindow(AppWindow) to be handled as a sub component
                 of the overall View of the program.

    '''
    def addComponents(self):
        #pass
        self.mainWindow.addTable(self.tableView.getTableWidget())
        #self.mainWindow.addVision()
        #self.mainWindow.addLog()
        #self.mainWindow.addGraph(graphOptions, GraphWidget)
        self.mainWindow.addSemiAuto(SemiAutoWidget(type(self).semiAutoUIPath))

    ''' 

        Function: connectActionsMainWindow(self)
        Parameters: self
        Return Value: N/A
        Purpose: connects Actions relating to the QMainWindow(AppWindow) that require a higher level scope
                 than what is normally allowed to AppWindow such as newfile, openfile, savefile, saveAs.

    '''
    def connectActionsMainWindow(self):
        #FileMenu
        self.mainWindow.actionNew.triggered.connect(self.newFile)
        self.mainWindow.actionOpen.triggered.connect(self.openFile)
        self.mainWindow.actionSave.triggered.connect(self.saveFile)
        self.mainWindow.actionSaveAs.triggered.connect(self.saveAsFile)
        # self.mainWindow.actionUpload.triggered.connect(self.upload)

        #Edit Menu
        self.mainWindow.actionAddCar.triggered.connect(self.addCar)

        #View Menu
        self.mainWindow.actionSemiAuto.triggered.connect(lambda e: type(self).toggleWidget(self.mainWindow.SemiAutoWidget,e))

        #Help Menu

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
        if(self.writeFile == None):
            self.writeFile = self.mainWindow.saveAsFileDialog()

        #else use writeFile

        #continue to dump save file


    ''' 

        Function: SaveAsFile(self)
        Parameters: self
        Return Value: N/A
        Purpose: Saves the current session of data from TableModel to the writeFile chosen by the user,
                 if the user doesn't choosen a filename, it'll asssume a default file name to save as under
                 the current working directory.

    '''
    def saveAsFile(self):
        self.writeFile = self.mainWindow.saveAsFileDialog()
        #write file to location

    ''' 

        Function: openFile(self)
        Parameters: self
        Return Value: N/A
        Purpose: opens a file chosen by the user via FileDialog that is then opened and read/parsed
                 into the Table Model

    '''
    def openFile(self):
        if(self.readFile == None):
            self.readFile = self.mainWindow.openFileDialog()

    ''' 

        Function: newFile(self)
        Parameters: self
        Return Value: N/A
        Purpose: Clears any currently existing tableModel, prompts user to set a filename via FileDialog,
                 then saves that as the current writeFile to be used for anything further.

    '''
    def newFile(self):
        self.writeFile = self.mainWindow.saveAsFileDialog()


    def addCar(self):
        newCar = self.mainWindow.addCarDialog()
        if newCar:
            newCar.ID = len(self.tableView.CarStoreList.storageList)
            self.tableView.CarStoreList.addExistingCar(newCar)
            self.mainWindow.SemiAutoWidget.addCar(newCar)

    # def upload(self):
    #     self.mainWindow.googleDriveDialog()





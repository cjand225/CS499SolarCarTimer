'''
    Module: App.py
    Purpose: Controller for entire application, used to periodically update project with data to and from the
             model.
    Depends On:

'''
# standard lib imports
import sys, os

# dependency imports
from PyQt5.QtWidgets import QApplication

# package imports
from SCTimeUtility.App import mainUIPath, quitDialogUIPath, helpDialogUIPath, aboutDialogUIPath, userManPath, \
    aboutManPath, adminManPath
from SCTimeUtility.App.AppWindow import AppWindow
from SCTimeUtility.Table.Table import Table
from SCTimeUtility.Video.Video import Video
from SCTimeUtility.Graph.Graph import Graph
from SCTimeUtility.LeaderBoard.LeaderBoard import LeaderBoard
from SCTimeUtility.Log.Log import get_log
from SCTimeUtility.Log.LogWidget import LogWidget
from SCTimeUtility.System.FileSystem import export_csv, import_csv


class App(QApplication):

    def __init__(self):
        super(App, self).__init__(sys.argv)
        self.application_window = None
        self.running = False

        # Forward Module Declaration
        self.logger = get_log()

        self.module_list = []

        self.table_module = None
        self.semi_auto_module = None
        self.vision_module = None
        self.graph_module = None
        self.log_module = None
        self.leaderboard_module = None

        # Initializing everything
        self.init_application()

    ''' 

        Function: initApplication(self)
        Parameters: self
        Return Value: N/A
        Purpose: Initializes the QApplication, required for running and maintaing program.

    '''

    def init_application(self):
        self.init_application_window()
        self.init_log_module()
        self.init_table_module()
        self.init_vision_module()
        self.init_graph_module()
        self.init_leaderboard_module()

        # adding and connecting essential components to user interface
        self.bind_components()
        self.bind_actions_application_window()

    ''' 

        Function: initMainWindow(self)
        Parameters: self
        Return Value: N/A
        Purpose: Initializes AppWindow in the mainWindow Variable attached to App Class as well as
                 Initializing any functions related to the AppWindow Class

    '''

    def init_application_window(self):
        self.application_window = AppWindow(mainUIPath)
        self.application_window.init_close_dialog(quitDialogUIPath)

        self.application_window.action_admin_manual.triggered.connect(
            lambda l: self.application_window.create_browser_dialog(helpDialogUIPath, adminManPath))
        self.application_window.action_about.triggered.connect(
            lambda l: self.application_window.create_browser_dialog(aboutDialogUIPath, aboutManPath))
        self.application_window.action_user_manual.triggered.connect(
            lambda l: self.application_window.create_browser_dialog(helpDialogUIPath, userManPath))

    ''' 

        Function: initTableview(self)
        Parameters: self
        Return Value: N/A
        Purpose: Initializes the Table Class (w/ a path to the view's UI), that is its own controller for handling 
                 both its internal model and View class (however view class is passed to AppWindow to handle afterwards)

    '''

    def init_table_module(self):
        self.table_module = Table()
        if self.table_module is not None:
            self.logger.debug('[' + __name__ + ']' + ' Table Initialized')
        else:
            self.logger.debug('[' + __name__ + ']' + ' Table failed to initialize')

    ''' 

        Function: initVision(self)
        Parameters: self
        Return Value: N/A
        Purpose: Initializes the Vision Class (w/ a path to the View's UI), that handled camera interfacing, image
                 processing, and OCR related tasks, which then can interface with the Table Class in order to update
                 Various Cars with Laptime Information

    '''

    def init_vision_module(self):
        self.vision_module = Video()
        if self.vision_module is not None:
            get_log().debug('[' + __name__ + '] ' + 'Video module Initialized')
        else:
            get_log().debug('[' + __name__ + '] ' + 'Video module failed to initialize')

    ''' 

        Function: initLog(self)
        Parameters: self
        Return Value: N/A
        Purpose: Initializes the Log Class (w/ a path to the View's UI and Writing directory), that handles
                 file writes to a specified file when the Log Class is invoked.

    '''

    def init_log_module(self):
        self.log_module = LogWidget()
        if self.log_module is not None:
            get_log().debug('[' + __name__ + '] ' + 'Log module initialized')
        else:
            get_log().debug('[' + __name__ + '] ' + 'Log module failed to initialize')

    ''' 

        Function: initGraph(self)
        Parameters: self
        Return Value: N/A
        Purpose: initializes the Graphing Module (w/ a path to the View's UI), which then when given information
                 in the form of lists and user specified information, can create Graphs via its own VieW

    '''

    def init_graph_module(self):
        self.graph_module = Graph()
        if self.graph_module is not None:
            get_log().debug('[' + __name__ + '] ' + 'Graph module initialized')
        else:
            get_log().debug('[' + __name__ + '] ' + 'Graph module failed to initialize')

    ''' 

        Function: initLeaderBoard(self)
        Parameters: self
        Return Value: N/A
        Purpose: initializes the LeaderBoard Module (w/ a path to the View's UI), which then when given information
                 in the form of lists of information based on racing data can create a visual list from its view for user.

    '''

    def init_leaderboard_module(self):
        self.leaderboard_module = LeaderBoard(self.table_module.car_storage_list)
        if self.leaderboard_module is not None:
            get_log().debug('[' + __name__ + '] ' + 'LeaderBoard module initialized')
        else:
            get_log().debug('[' + __name__ + '] ' + 'LeaderBoard module failed to initialize')

    ''' 

        Function: addComponents(self)
        Parameters: self
        Return Value: N/A
        Purpose: Adds widgets from each module to mainWindow(AppWindow) to be handled as a sub component
                 of the overall View of the program.

    '''

    def bind_components(self):
        get_log().debug('[' + __name__ + '] ' + 'Adding components to Main Window')

        if self.log_module is not None:
            self.application_window.add_log(self.log_module)
        if self.table_module is not None:
            self.application_window.add_table(self.table_module.get_table_widget())
        if self.table_module.get_semi_auto_module() is not None:
            self.application_window.add_semi_auto(self.table_module.get_semi_auto_module())
        if self.vision_module is not None:
            self.application_window.add_vision(self.vision_module.get_widget())
        if self.graph_module is not None:
            self.application_window.add_graph(self.graph_module)
        if self.leaderboard_module is not None:
            self.application_window.add_leaderboard(self.leaderboard_module.get_widget())

        self.application_window.bind_components()

    ''' 

        Function: connectActionsMainWindow(self)
        Parameters: self
        Return Value: N/A
        Purpose: connects Actions relating to the QMainWindow(AppWindow) that require a higher level scope
                 than what is normally allowed to AppWindow such as newfile, openfile, savefile, saveAs.

    '''

    def bind_actions_application_window(self):
        get_log().debug('[' + __name__ + '] ' + 'Binding listeners to Main Window')
        self.application_window.action_new.triggered.connect(self.new_session)
        self.application_window.action_open.triggered.connect(self.import_data)
        self.application_window.action_export.triggered.connect(self.export_data)
        #self.table.widget.save_shortcut_binding.activated.connect(self.exportDataToFile)
        self.table_module.car_storage_list.dataModified.connect(self.update_graph)

    ''' 
    
        Function: run(self)
        Parameters: self
        Return Value: N/A
        Purpose: Runs entire Program until Application returns from executing, which then closes with a 
                 proper exit code.

    '''

    def run(self):
        self.running = True
        sys.exit(self.exec_())

    ''' 

        Function: SaveAsFile(self)
        Parameters: self
        Return Value: N/A
        Purpose: Saves the current session of data from TableModel to the writeFile chosen by the user,
                 if the user doesn't choose a filename, it'll assume a default file name to save as under
                 the current working directory.

    '''

    def export_data(self):
        write_path = os.path.join(self.application_window.open_directory_dialog())
        if os.path.exists(write_path):
            export_csv(self.table_module.car_storage_list, write_path)
            self.logger.debug('[' + __name__ + '] ' + 'Data saved to: ' + write_path)
        else:
            self.logger.debug('[' + __name__ + '] ' + 'Could not save data to: ' + str(write_path))

    ''' 

        Function: importDataFromFile(self)
        Parameters: self
        Return Value: N/A
        Purpose: opens a directory chosen by user, then proceeds to read and parse CSVs that have relevant tokens
                 and data. 

    '''

    # TODO: Rework so that add_car passes in Table module data
    def import_data(self):
        read_directory = os.path.join(self.application_window.open_directory_dialog())
        if os.path.exists(read_directory):
            import_csv(read_directory)
        else:
            pass

    ''' 

        Function: newSession(self)
        Parameters: self
        Return Value: N/A
        Purpose: Clears any currently existing Table module, allowing for application to essentially restart.

    '''

    def new_session(self):
        if not self.table_module.car_storage_list:
            self.logger.debug('[' + __name__ + '] ' + 'Started new session requested by user: ')
        else:
            self.logger.debug('[' + __name__ + '] ' + 'Failed to create new session.')

    '''
        Function: graphUpdate
        Parameters: self
        Return Value: N/A
        Purpose: Binds an update function to pass a copy of carStorage to the graph if the table is ever updated with
                 new information (based on qt signals emitted by cars).
    
    '''

    def update_graph(self):
        self.graph_module.handle_update(self.table_module.get_car_storage())

    '''
        Function: graphUpdate
        Parameters: self
        Return Value: N/A
        Purpose: Binds an update function to pass a copy of carStorage to the leaderboard if the table is ever updated 
                 with new information (based on qt signals emitted by cars).

    '''

    def update_leaderboard(self):
        self.leaderboard_module.update_data(self.table_module.get_car_storage())

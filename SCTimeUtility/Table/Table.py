"""

    Module:
    Purpose:
    Depends On:

"""

import datetime

from PyQt5.QtWidgets import QDialog

from SCTimeUtility.Table import tableUIPath, semiAutoUIPath, addCarDialogUIPath, addBatchCarDialogUIPath
from SCTimeUtility.Table.CarStorage import CarStorage
from SCTimeUtility.Table.TableModel import TableModel
from SCTimeUtility.Table.TableWidget import TableWidget
from SCTimeUtility.Table.AddCarDialog import AddCarDialog
from SCTimeUtility.Table.AddBatchDialog import AddBatchDialog
from SCTimeUtility.Table.SemiAuto import SemiAuto
from SCTimeUtility.Log.Log import get_log


class Table():

    def __init__(self):
        super().__init__()

        self.logger = get_log()
        # things to be initialized later
        self.TableMod = None
        self.widget = None
        self.car_storage_list = None
        self.save_shortcut_binding = None
        self.table_view = None
        self.semi_auto_module = None
        self.semi_auto_widget = None
        self.add_car_dialog = None
        self.add_multi_car_dialog = None

        self.init_table_module()

    '''

        Function: initUI
        Parameters: self
        Return Value: N/A
        Purpose: Initializes and loads the gui related Resources for Table class module.

    '''

    def init_widget(self):
        self.widget = TableWidget(tableUIPath)
        self.widget.init_vertical_header()
        self.widget.show()
        self.table_view = self.widget.table_view

    '''

        Function: connectActions
        Parameters: self
        Return Value: N/A
        Purpose: connects all the necessary signals to their functions for use during runtime.

    '''

    def bind_actions(self):
        self.table_view.doubleClicked.connect(self.double_click_event)

        self.widget.add_car_pb.clicked.connect(self.add_car_event)
        self.widget.add_multi_pb.clicked.connect(self.add_multi_car_event)
        # self.Widget.edit_car_pb.clicked.connect(self.editCar)
        # self.Widget.remove_car_pb.clicked.connect(self.removeCar)
        # self.Widget.start_car_pb.clicked.connect()
        # self.Widget.stop_car_pb.clicked.connect()

        self.car_storage_list.dataModified.connect(self.update_semi_auto_module)
        self.car_storage_list.dataModified.connect(self.resize_headers)

        self.semi_auto_module.globalStart.clicked.connect(self.car_storage_list.start_all_cars)
        self.semi_auto_module.globalStop.clicked.connect(self.car_storage_list.stop_all_cars)
        self.semi_auto_module.addCar.clicked.connect(self.add_car_event)
        # self.semiAuto.editCar.clicked.connect()
        self.semi_auto_module.addMultiple.clicked.connect(self.add_multi_car_event)
        # self.semiAuto.removeCar.clicked.connect()

    '''

        Function: getTableWidget
        Parameters: self
        Return Value: TableWidget class instance
        Purpose: Returns the instance of TableWidget stored within the Table Class instance.

    '''

    def get_table_widget(self):
        return self.widget

    '''

        Function: initTableModel
        Parameters: self
        Return Value: N/A
        Purpose: Initializes an instance of the TableModel Class for usage within the Table Class Module.

    '''

    def get_table_model(self):
        self.TableMod = TableModel(self.widget, self.car_storage_list)
        self.table_view.setModel(self.TableMod)

    '''

        Function: initTable
        Parameters: self
        Return Value: N/A
        Purpose: Initializes all the functional parts related to the Table class, when an instance of it is created.

    '''

    def init_table_module(self):
        # Model > UI > UIModel
        self.init_car_storage()
        self.init_widget()
        self.get_table_model()
        self.resize_headers()
        self.init_dialogs()
        self.init_semi_auto_module()
        self.bind_actions()

    '''

        Function: initCarStorage
        Parameters: self
        Return Value: N/A
        Purpose: Initializes an instance of the CarStorage Class, used as a backend for storing App data.

    '''

    def init_car_storage(self):
        self.car_storage_list = CarStorage()

    '''

        Function: getCarStorage
        Parameters: self
        Return Value: CarStorage Class Instance
        Purpose: Returns a CarStorage class Instance copy to invoker.

    '''

    def get_car_storage(self):
        return self.car_storage_list.car_list_copy()

    '''

        Function: initSemiAuto
        Parameters: self
        Return Value: N/A
        Purpose: Initializes the Semi Auto class (w/ path to view's UI) that is its own controller for handling
                 semi-automatic recording times for the Table.

    '''

    def init_semi_auto_module(self):
        self.semi_auto_module = SemiAuto(semiAutoUIPath)
        self.logger.debug('[' + __name__ + '] ' + 'Semi-Auto Initialized')

    '''

        Function: getSemiAuto
        Parameters: self
        Return Value: SemiAuto class instance
        Purpose: Returns the instance of the SemiAuto class declared within the Table class module to invoker.

    '''

    def get_semi_auto_module(self):
        return self.semi_auto_module

    '''

        Function: initDialogs
        Parameters: self
        Return Value: N/A
        Purpose: Initializes dialogs used for adding car data to Table module.

    '''

    def init_dialogs(self):
        self.add_car_dialog = AddCarDialog(addCarDialogUIPath)
        self.add_multi_car_dialog = AddBatchDialog(addBatchCarDialogUIPath)

    '''

        Function: createCar
        Parameters: self
        Return Value: N/A
        Purpose: Wrapper function to pass data onto CarStorage's createCar function.
        
    '''

    def create_car(self, carNum, teamName):
        self.car_storage_list.create_car(carNum, teamName)

    '''

        Function: createCars
        Parameters: self
        Return Value: N/A
        Purpose: Wrapper function to pass data onto CarStorage's createCars function.

    '''

    def create_multiple_cars(self, list):
        self.car_storage_list.create_multiple_cars(list)

    '''

        Function: handleStart
        Parameters: self
        Return Value: N/A
        Purpose: Sets a seed value when GlobalStart is Clicked.

    '''

    def enable_car_start(self):
        self.car_storage_list.set_seed_value(datetime.datetime.now())

    '''

        Function: handleTableDoubleClick
        Parameters: self, i
        Return Value: N/A
        Purpose: Invokes the handleAddDialog function when clicking on an unpopulated column.

    '''

    def double_click_event(self, i):
        if i.column() == len(self.car_storage_list.storage_list):
            self.add_car_event()

    '''

        Function: handleAddDialog
        Parameters: self
        Return Value: N/A
        Purpose: Invokes the actual Dialog to probe user for car information.

    '''

    def add_car_event(self):
        ret_val = self.add_car_dialog.exec()
        if ret_val == QDialog.Accepted:
            self.create_car(self.add_car_dialog.carNumber, self.add_car_dialog.teamName)
            self.add_car_dialog.clearText()

    '''

        Function: handleAddBatchDialog
        Parameters: self
        Return Value: N/A
        Purpose: Invokes the actual Dialog to probe user for car information of multiple cars.

    '''

    def add_multi_car_event(self):
        ret_val = self.add_multi_car_dialog.exec()
        if ret_val == QDialog.Accepted:
            self.create_multiple_cars(self.add_multi_car_dialog.get_list())
            self.add_multi_car_dialog.clear_batch()

    '''
    
        Function: handleStart
        Parameters: self
        Return Value: N/A
        Purpose: Updates SemiAuto with new information from within the CarStorage Module

    '''

    def update_semi_auto_module(self):
        self.semi_auto_module.update_list(self.car_storage_list.storage_list)

    '''

        Function: adjustHeaders
        Parameters: self
        Return Value: N/A
        Purpose: Temp fix for widget stuff

    '''

    def resize_headers(self):
        self.widget.init_horizontal_header()
        self.widget.init_vertical_header()

    # TODO
    def remove_car(self):
        pass

    # TODO
    def edit_car_details(self):
        pass

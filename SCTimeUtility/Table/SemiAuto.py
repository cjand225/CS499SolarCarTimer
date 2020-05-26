"""

    Module:
    Purpose:
    Depends On:

"""
from PyQt5.QtWidgets import QWidget, QApplication, QStyle, QPushButton, QCheckBox
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi

from collections import OrderedDict

from SCTimeUtility.Table.ElidedLabel import ElidedLabel
from SCTimeUtility.Log.Log import get_log


class SemiAuto(QWidget):

    def __init__(self, resource_path):
        super().__init__()
        self.resource_path = resource_path

        self.car_storage = None
        self.car_storage_reference = []

        # column positions of buttons in dict and on widget
        self.car_label = 0
        self.record_action_button = 1
        self.time_prediction_label = 2
        self.prediction_check_box = 3
        self.start_button = 4

        # holds dicts related to each car
        self.button_dictionary = OrderedDict()

        # layout of semiAuto
        self.buttons = None

        self.init_widget()
        self.init_button_layout()
        self.create_buttons()

    '''  
        Function: initUI
        Parameters: self
        Return Value: N/A
        Purpose: Initializes and loads Resources for SemiAuto Widget.
    '''

    def init_widget(self):
        self.widget = loadUi(self.resource_path, self)
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignRight,
                                            self.size(), QApplication.desktop().availableGeometry()))
        self.buttons = self.buttonsLayout
        self.move(self.x(), self.y())

    '''  
        Function: initButtonLayout
        Parameters: self
        Return Value: N/A
        Purpose: Initializes the layout and placement of individual buttons needed for control of each car.
    '''

    def init_button_layout(self):
        self.buttons.setAlignment(Qt.AlignTop)
        self.buttons.setColumnMinimumWidth(self.car_label, 100)
        self.buttons.setColumnMinimumWidth(self.time_prediction_label, 100)
        self.buttons.setHorizontalSpacing(15)
        self.buttons.setColumnStretch(self.car_label, 1)
        self.buttons.setColumnStretch(self.record_action_button, 1)
        self.buttons.setColumnStretch(self.time_prediction_label, 0)

    '''  
        Function: updateList
        Parameters: self, list
        Return Value: N/A
        Purpose: Calls all the relevant functions need to re-create the widget controls based on amount of cars.
    '''

    def update_list(self, list):
        self.clear_lists()
        self.car_storage_reference = list
        self.create_buttons()
        # self.createPredictionLabels()
        self.bind_buttons()
        self.add_buttons()

    '''  
        Function: createButtons
        Parameters: self
        Return Value: N/A
        Purpose: creates the actual row for each car control
    '''

    def create_buttons(self):
        label_index = 0
        for car in self.car_storage_reference:
            # create Label
            label = ElidedLabel()
            label.setText(str(car.getTeam()))
            label.setMaximumWidth(150)

            button = QPushButton()
            button.setText("Record Time")
            button.setObjectName(str(label_index))
            button.setMaximumWidth(150)

            check_box = QCheckBox()
            check_box.setText("Lap Prediction ")

            start_stop_button = QPushButton()
            start_stop_button.setText("Start")
            start_stop_button.setMaximumWidth(150)

            predict_label = ElidedLabel()
            predict_label.setText("0:00:00")
            predict_label.setHidden(True)

            self.button_dictionary.update({label_index: [label, button, predict_label, check_box, start_stop_button]})

            label_index += 1

    '''  
        Function: clearLists
        Parameters: self
        Return Value: N/A
        Purpose: unbinds all the signals, clears layout of widget, clears all logical lists needed to create
                 car controls.
    '''

    def clear_lists(self):
        self.remove_button_bindings()
        self.button_dictionary.clear()
        self.clear_layout(self.buttons)

    '''  
        Function: unBindButtons
        Parameters: self
        Return Value: N/A
        Purpose: Unbinds each button within their corresponding lists, allowing them to be re-bound at a later time.
    '''

    def remove_button_bindings(self):
        for buttonList in self.button_dictionary:
            self.button_dictionary[buttonList][self.record_action_button].clicked.disconnect()
            self.button_dictionary[buttonList][self.start_button].clicked.disconnect()
            self.button_dictionary[buttonList][self.prediction_check_box].toggled.disconnect()

    '''  
        Function: clearLayout
        Parameters: self, layout
        Return Value: N/A
        Purpose: Deleted widgets and cycles through sub-items to ensure proper deletion in order for more to be 
                 added at a later time.
    '''

    def clear_layout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clear_layout(item.layout())

    '''  
        Function: bindButtons
        Parameters: self
        Return Value: N/A
        Purpose: Wrapper to bind functions of Cars related to recording, starting and stopping to buttons within the 
                 widget.
    '''

    def bind_buttons(self):
        for buttonList in self.button_dictionary:
            self.bind_record_action(buttonList, self.button_dictionary[buttonList][self.record_action_button])
            self.bind_start_stop_action(buttonList, self.button_dictionary[buttonList][self.start_button])
            self.bind_prediction_action(buttonList, self.button_dictionary[buttonList][self.prediction_check_box])

    def add_buttons(self):
        for buttonList in self.button_dictionary:
            self.buttons.addWidget(self.button_dictionary[buttonList][self.car_label], buttonList, self.car_label)
            self.buttons.addWidget(self.button_dictionary[buttonList][self.record_action_button], buttonList, self.record_action_button)
            self.buttons.addWidget(self.button_dictionary[buttonList][self.start_button], buttonList, self.start_button)
            self.buttons.addWidget(self.button_dictionary[buttonList][self.time_prediction_label], buttonList, self.time_prediction_label)
            self.buttons.addWidget(self.button_dictionary[buttonList][self.prediction_check_box], buttonList, self.prediction_check_box)

    '''  
        Function: bindButtons
        Parameters: self, index, button
        Return Value: N/A
        Purpose: Binds button to the corresponding index given in parameters located within the button list.
    '''

    def bind_record_action(self, index, button):
        button.clicked.connect(lambda b: self.record_click_event(index))

    '''  
        Function: bindCheckBox
        Parameters: self, index, checkBox
        Return Value: N/A
        Purpose: Binds a given checkbox to their corresponding index within checkbox list.
    '''

    # TODO:
    def bind_prediction_action(self, index, checkBox):
        checkBox.toggled.connect(lambda b: self.check_action_enabled(self.car_storage_reference[index].ID))

    # TODO:
    def bind_start_stop_action(self, index, button):
        button.clicked.connect(lambda b: self.toggle_enable_car_event(self.car_storage_reference[index].ID))

    # TODO
    def bind_running(self, index):
        car = self.car_storage_reference[index]
        car.runningSignal.connect(lambda b: self.start_stop_click_event(self.car_storage_reference[index].ID))

    '''  
        Function: handleCheck
        Parameters: self, index
        Return Value: N/A
        Purpose: function used to calculate prediction times if a given checkbox is clicked for a particular car.
    '''

    def check_action_enabled(self, ID):
        if self.button_dictionary[ID][self.prediction_check_box].isChecked():
            self.button_dictionary[ID][self.time_prediction_label].setVisiible(True)
            # put handle calculation function here
        else:
            self.button_dictionary[ID][self.time_prediction_label].setHidden(True)

    '''  
        Function: clickRecord
        Parameters: self, index
        Return Value: N/A
        Purpose: Given the particular index, tells the CarStorage to add a laptime to that particular car index.
    '''

    def record_click_event(self, ID):
        self.car_storage_reference[ID].addLapTime()

    '''  
        Function: clickStartStop 
        Parameters: self, index
        Return Value: N/A
        Purpose: used for starting and stopping individual cars.
    '''

    def start_stop_click_event(self, ID):
        if not self.car_storage_reference[ID].is_running():
            self.button_dictionary[ID][self.start_button].setText("Start")
        else:
            self.button_dictionary[ID][self.start_button].setText("Stop")

    '''  
        Function: toggleCar
        Parameters: self, index
        Return Value: N/A
        Purpose: used for starting and stopping individual cars.
    '''

    def toggle_enable_car_event(self, ID):
        if self.car_storage_reference[ID].is_running():
            self.car_storage_reference[ID].stop()
            # Disabled Buttons for specific car
            self.button_dictionary[ID][self.record_action_button].setDisabled(True)
            self.button_dictionary[ID][self.prediction_check_box].setDisabled(True)
        elif not self.car_storage_reference[ID].is_running():
            self.car_storage_reference[ID].start()
            # Re-enable buttons for specific car
            self.button_dictionary[ID][self.record_action_button].setDisabled(False)
            self.button_dictionary[ID][self.prediction_check_box].setDisabled(False)

"""

    Module:
    Purpose:
    Depends On:

"""

# Standard Lib imports
from operator import itemgetter

# Dependency Imports
from PyQt5.QtCore import Qt, QSize

# Package Imports
from SCTimeUtility.LeaderBoard import LeaderBoardUIPath
from SCTimeUtility.LeaderBoard.LeaderBoardWidget import LeaderBoardWidget
from SCTimeUtility.LeaderBoard.LeaderBoardModel import LeaderBoardModel
from SCTimeUtility.LeaderBoard.LeaderBoardSortFilterProxyModel import LeaderBoardSortFilterProxyModel


class LeaderBoard:

    def __init__(self, cs=None):
        self.widget = None
        self.data_storage = None
        self.horizontal_header = ['Car Number', 'Team Name', 'Laps Completed', 'Fastest Lap']
        self.sortable_columns = [2, 3]
        self.car_list_copy = [[]]

        self.init_widget()
        self.carStore = cs
        self.boardModel = LeaderBoardSortFilterProxyModel(self.widget.table_view, self.sortable_columns)
        self.boardModel.setSourceModel(LeaderBoardModel(self.widget.table_view, self.horizontal_header, self.carStore))
        self.boardModel.setSortRole(Qt.UserRole)
        self.widget.table_view.setSortingEnabled(True)
        self.boardModel.sourceModel().dataChanged.connect(self.sort)
        self.widget.table_view.horizontalHeader().sortIndicatorChanged.connect(self.sort_indicator_changed_event)
        self.widget.table_view.setModel(self.boardModel)
        self.widget.resize_headers(True)
        self.widget.table_view.sortByColumn(3, Qt.AscendingOrder)

    '''  
        Function: sort
        Parameters: self
        Return Value: N/A
        Purpose: sorts the Model based on whats been clicked
    '''

    def sort(self):
        old_sort = self.boardModel.sortColumn()
        self.boardModel.invalidate()
        self.widget.table_view.sortByColumn(old_sort, Qt.AscendingOrder)

    '''  
        Function: sortIndicatorChangedEvent
        Parameters: self, index, order
        Return Value: N/A
        Purpose: checks if index is within the alotted columns and then indicates that a sort event has happened.
    '''

    def sort_indicator_changed_event(self, index, order):
        if not index in self.sortable_columns:
            self.widget.table_view.horizontalHeader().setSortIndicator(index, self.boardModel.sortOrder())

    '''  
        Function: initWidget
        Parameters: self
        Return Value: N/A
        Purpose: Initializes the widget for the leader board module.
    '''

    def init_widget(self):
        self.widget = LeaderBoardWidget(LeaderBoardUIPath)

    '''  
        Function: get_widget
        Parameters: self
        Return Value: self.widget
        Purpose: Returns a reference to the widget stored within the LeaderBoard Module.
    '''

    def get_widget(self):
        return self.widget

    '''  
        Function: updateData
        Parameters: self, data
        Return Value: N/A
        Purpose: Periodically called function used to update the data contained within leader board module.
    '''

    def update_data(self, data):
        self.data_storage = data
        self.update_board(data)
        self.sort_by_fastest()

    '''  
        Function: testLap
        Parameters: self
        Return Value: N/A
        Purpose: test function used to check the sorting by fastest lap function.
    '''

    def test_lap(self):
        self.sort_by_fastest()

    '''  
        Function: sortCar
        Parameters: self
        Return Value: N/A
        Purpose: Interates through the cars within datastorage and gets their fastest lap, appending it to a list
                 and updating the board based on that.
    '''

    def sort_by_fastest(self):
        self.car_list_copy = [[]]
        self.car_list = []
        self.car_list.clear()
        self.car_list_copy.clear()

        for car in self.data_storage:
            listCar = [car.getID(), car.getFastestLap()]
            self.car_list_copy.append(listCar)
            if itemgetter(1) is not None:
                self.car_list_copy = sorted(self.car_list_copy, key=itemgetter(1))

        for x in range(0, len(self.car_list_copy)):
            self.car_list.append(self.data_storage[self.car_list_copy[x][0]])

        self.update_board(self.car_list)

    '''  
        Function: updateBoard
        Parameters: self, data
        Return Value: N/A
        Purpose: Updates the view of the leader board module with the data supplied from the parameter.
    '''

    def update_board(self, data):
        self.widget.resize(QSize(self.widget.width() + 1, self.widget.height()))
        self.boardModel.setModelData(data)
        self.widget.init_horizontal_header()
        self.widget.init_vertical_header()
        self.widget.resize(QSize(self.widget.width() - 1, self.widget.height()))

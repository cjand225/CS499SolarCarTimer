"""

    Module:
    Purpose:
    Depends On:

"""

from PyQt5.QtCore import Qt, QSortFilterProxyModel


class LeaderBoardSortFilterProxyModel(QSortFilterProxyModel):

    def __init__(self, parent, sortable_columns):
        super().__init__(parent)
        self.sortable_columns = sortable_columns

    '''  
        Function: lessThan
        Parameters: self, sourceLeft, sourceRight
        Return Value: Boolean or QSortFilterProxyModel.lessThan(sourceLeft, sourceRight)
        Purpose: Checks whether than parameters are given, if they are, calls the less than
                 function inherited from QSortFilterProxyModel.
    '''

    def lessThan(self, source_left, source_right):
        if source_left.data(Qt.UserRole) is None:
            return False
        elif source_right.data(Qt.UserRole) is None:
            return False
        else:
            return super().lessThan(source_left, source_right)

    '''  
        Function: sort
        Parameters: self, column, order
        Return Value: N/A
        Purpose: sorts the data of the leaderboard based on the order given or a default ordering, to the column
                 provided.
    '''

    def sort(self, column, order=Qt.AscendingOrder):
        if column in self.sortable_columns:
            super().sort(column, order)

    '''  
        Function: headerData
        Parameters: self, section, orientation, role
        Return Value: HeaderData
        Purpose: populated the headers based on orientation, section, and role of each header for the leaderboard
                 view.
    '''

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Vertical:
                if self.sortOrder() == Qt.AscendingOrder:
                    return self.sourceModel().headerData(section, orientation, Qt.UserRole)
                else:
                    return self.sourceModel().headerData(section, orientation, Qt.UserRole + 1)
            else:
                return self.sourceModel().headerData(section, orientation, Qt.DisplayRole)

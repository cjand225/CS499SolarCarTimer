"""

    Module:
    Purpose:
    Depends On:

"""

from PyQt5.QtCore import Qt, QSortFilterProxyModel


class LeaderBoardSortFilterProxyModel(QSortFilterProxyModel):

    def __init__(self, parent, sortableColumns):
        super().__init__(parent)
        self.sortableColumns = sortableColumns

    '''  
        Function: lessThan
        Parameters: self, sourceLeft, sourceRight
        Return Value: Boolean or QSortFilterProxyModel.lessThan(sourceLeft, sourceRight)
        Purpose: Checks whether than parameters are given, if they are, calls the less than
                 function inherited from QSortFilterProxyModel.
    '''

    def lessThan(self, sourceLeft, sourceRight):
        if sourceLeft.data(Qt.UserRole) is None:
            return False
        elif sourceRight.data(Qt.UserRole) is None:
            return False
        else:
            return super().lessThan(sourceLeft, sourceRight)

    '''  
        Function: sort
        Parameters: self, column, order
        Return Value: N/A
        Purpose: sorts the data of the leaderboard based on the order given or a default ordering, to the column
                 provided.
    '''

    def sort(self, column, order=Qt.AscendingOrder):
        if column in self.sortableColumns:
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

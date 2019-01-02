from PyQt5.QtCore import Qt, QSortFilterProxyModel


class LeaderBoardSortFilterProxyModel(QSortFilterProxyModel):
    def __init__(self, parent, sortableColumns):
        super().__init__(parent)
        self.sortableColumns = sortableColumns

    def lessThan(self, sourceLeft, sourceRight):
        # print(sourceLeft)
        if sourceLeft.data(Qt.UserRole) is None:
            # print("left",sourceRight.data(Qt.UserRole),sourceLeft.data(Qt.UserRole))
            return False
        elif sourceRight.data(Qt.UserRole) is None:
            # print("right",sourceRight.data(Qt.UserRole),sourceLeft.data(Qt.UserRole))
            return False
        else:
            # print(sourceRight.data(Qt.UserRole),sourceLeft.data(Qt.UserRole))
            return super().lessThan(sourceLeft, sourceRight)

    def sort(self, column, order=Qt.AscendingOrder):
        if column in self.sortableColumns:
            super().sort(column, order)

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Vertical:
                if self.sortOrder() == Qt.AscendingOrder:
                    return self.sourceModel().headerData(section, orientation, Qt.UserRole)
                else:
                    return self.sourceModel().headerData(section, orientation, Qt.UserRole + 1)
            else:
                return self.sourceModel().headerData(section, orientation, Qt.DisplayRole)

import unittest
import sys
from src.table.Table import Table
from PyQt5.QtWidgets import QApplication, QMainWindow



class TestTableMethods(unittest.TestCase):

    def setUp(self):
        self.app = QApplication(sys.argv)
        self.window = QMainWindow()
        self.window.table = Table()

    '''
     tests for proper horizontal headers
    '''
    def test_headerH(self):
        list = ["hi", "blah", "132"]
        self.window.table.setColumnNames(list)
        for x in range(0, len(list)):
            self.assertEqual(self.window.table.getTableWidget().horizontalHeaderItem(x).text(), list[x])

    #checks format of Headers and if they're set
    #specifically if they are alphanumeric and if they're names
    def test_verticalH(self):
        list = ["hi", "blah", "1"]
        self.window.table.setColumnNames(list)
        for x in range(1, len(list)):
            self.assertTrue(self.window.table.getTableWidget().horizontalHeaderItem(x).text())

    def test_cell_text_format(self):
        self.window.table.setCell(0,0, "hi")
        self.assertNotEqual(self.window.table.getCell(0,0), "hi")




if __name__ == '__main__':
    unittest.main()






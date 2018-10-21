import unittest
import sys
from src.table.Table import Table
from PyQt5.QtWidgets import QApplication, QMainWindow



class TestStringMethods(unittest.TestCase):

    def setUp(self):
        self.app = QApplication(sys.argv)
        self.window = QMainWindow()
        self.window.table = Table()

    #def tearDown(self):

    def test_headerH(self):
        list = ["hi", "blah"]
        self.window.table.setColumnNames(list)
        for x in range(1, len(list)):
            self.assertEqual(self.window.table.getTableWidget().horizontalHeaderItem(x).text(), list[x])

    #tests for vertical headers to see if correct
    #def text_verticalH(self):



if __name__ == '__main__':
    unittest.main()






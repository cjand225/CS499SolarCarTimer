import unittest, sys

from PyQt5.QtWidgets import QMainWindow, QApplication

from SCTimeUtility.app.App import App
from SCTimeUtility.table.Table import Table


class TestAppMethods(unittest.TestCase):

    def setUp(self):
        self.App = QApplication(sys.argv)
        self.AppWindow = QMainWindow()

    def testCreateTable(self):
        self.testTable = Table()
        self.assertNotEqual(self.testTable, None)

import unittest
import sys
from SCTimeUtility.app.App import App
from SCTimeUtility.table.Table import Table

from PyQt5.Qt import QApplication
from PyQt5.QtWidgets import QMainWindow


class TestAppMethods(unittest.TestCase):

    def setUp(self):
        self.App = QApplication()
        self.AppWindow = QMainWindow()

    def testCreateTable(self):
        self.testTable = Table()
        self.assertNotEqual(self.testTable, None)

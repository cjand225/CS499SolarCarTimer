import unittest
import sys
from src.app.App import App
from src.app.AppWindow import AppWindow
from PyQt5.QtWidgets import QApplication, QMainWindow

class TestAppMethods(unittest.TestCase):

    def testCreatApplication(self):
        self.App = App()
        self.assertNotEqual(self.App, None)

    def testNotRunning(self):
        self.App = App()
        self.assertEqual(self.App.isRunning(), False)

    def testMainWindowCreation(self):
        self.App = App()
        self.assertNotEqual(self.App.getMainWindow(), None)

    def testVideoModule(self):
        self.App = App()
        self.assertNotEqual(self.App.videoMod, None)

    def testTableModule(self):
        self.App = App()
        self.assertNotEqual(self.App.tableMod, None)
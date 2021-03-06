import unittest, sys
from SCTimeUtility.App.App import App
from SCTimeUtility.App.AppWindow import AppWindow
from PyQt5.QtWidgets import QApplication, QMainWindow


class TestAppMethods(unittest.TestCase):

    def testCreatApplication(self):
        self.App = App()
        self.assertNotEqual(self.App, None)

    def testNotRunning(self):
        self.App = App()
        self.assertEqual(self.App.running, False)

    def testMainWindowCreation(self):
        self.App = App()
        self.assertNotEqual(self.App.mainWindow, None)

    def testVideoModule(self):
        self.App = App()
        self.assertNotEqual(self.App.vision, None)

    def testTableModule(self):
        self.App = App()
        self.assertNotEqual(self.App.table, None)

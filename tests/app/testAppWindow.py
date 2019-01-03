import unittest
import sys
from SCTimeUtility.app.App import App
from SCTimeUtility.app.AppWindow import AppWindow
from SCTimeUtility.table.SemiAuto import SemiAuto
from SCTimeUtility.table.Table import Table
from SCTimeUtility.video.VideoWidget import VisionWidget
from SCTimeUtility.log.LogWidget import LogWidget
from SCTimeUtility.graph.Graph import Graph


class TestAppWindowMethods(unittest.TestCase):

    def setUp(self):
        self.MyApp = App()
        self.MyAppWindow = self.MyApp.mainWindow

    def testAddVision(self):
        vis = VisionWidget(App.visionUIPath)
        self.MyAppWindow.addVision(vis)
        self.assertTrue(self.MyAppWindow.visionWidget, vis)

    def testAddTable(self):
        mytable = Table()
        self.MyAppWindow.addTable(mytable)
        self.assertTrue(self.MyAppWindow.tableWidget, mytable)

    def testAddLog(self):
        myLog = LogWidget(App.logUIPath)
        self.MyAppWindow.addLog(myLog)
        self.assertTrue(self.MyAppWindow.logWidget, myLog)

    def testaddSemiAuto(self):
        mySemi = SemiAuto(Table.semiAutoUIPath)
        self.MyAppWindow.addSemiAuto(mySemi)
        self.assertTrue(self.MyAppWindow.semiAutoWidget, mySemi)

    def testAddGraphWidget(self):
        myGraph = Graph(App.graphUIPath)
        self.MyAppWindow.addGraph(myGraph)
        self.assertTrue(self.MyAppWindow.graphWidget, myGraph)

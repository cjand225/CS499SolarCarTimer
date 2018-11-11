import unittest
import sys
from src.app.App import App
from src.app.AppWindow import AppWindow
from src.table.SemiAutoWidget import SemiAutoWidget
from src.table.Table import Table
from src.video.VisionWidget import VisionWidget
from src.log.LogWidget import LogWidget
from src.graph.GraphWidget import Graph
from src.graph.GraphOptionsWidget import GraphOptions

class TestAppWindowMethods(unittest.TestCase):

    def setUp(self):
        self.MyApp = App()
        self.MyAppWindow = self.MyApp.mainWindow

    def testAddVision(self):
        vis = VisionWidget(App.visionUIPath)
        self.MyAppWindow.addVison(vis)
        self.assertTrue(self.MyAppWindow.VisionWidget, vis)

    def testAddTable(self):
        mytable = Table(App.tableUIPath)
        self.MyAppWindow.addTable(mytable)
        self.assertTrue(self.MyAppWindow.TableWidget, mytable)

    def testAddLog(self):
        myLog = LogWidget(App.logUIPath)
        self.MyAppWindow.addLog(myLog)
        self.assertTrue(self.MyAppWindow.LogWidget, myLog)

    def testaddSemiAuto(self):
        mySemi = SemiAutoWidget(App.semiAutoUIPath)
        self.MyAppWindow.addSemiAuto(mySemi)
        self.assertTrue(self.MyAppWindow.SemiAutoWidget, mySemi)

    def testAddGraphWidget(self):
        myGraph = Graph(App.quitDialogPath)
        self.MyAppWindow.addGraph(myGraph)
        self.assertTrue(self.MyAppWindow.GraphWidget, myGraph)

    def testAddGraphOptionsWidget(self):
        myGraphOps = GraphOptions(App.graphOptionsPath)
        self.MyAppWindow.addGraphOptions(myGraphOps)
        self.assertTrue(self.MyAppWindow.GraphOptionsWidget, myGraphOps)

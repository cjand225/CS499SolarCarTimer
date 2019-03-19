import unittest
import sys
from SCTimeUtility.App.App import App
from SCTimeUtility.Table.SemiAuto import SemiAuto
from SCTimeUtility.Table.Table import Table
from SCTimeUtility.Video.VideoWidget import VideoWidget
from SCTimeUtility.Log.LogWidget import LogWidget
from SCTimeUtility.Graph.Graph import Graph
from SCTimeUtility.Resources.UI import semiAutoPath, graphWidPath, tableViewPath, videoPath, logWidPath


class TestAppWindowMethods(unittest.TestCase):

    def setUp(self):
        self.MyApp = App()
        self.MyAppWindow = self.MyApp.mainWindow

    def testAddVision(self):
        vis = VideoWidget(videoPath)
        self.MyAppWindow.addVision(vis)
        self.assertTrue(self.MyAppWindow.visionWidget, vis)

    def testAddTable(self):
        mytable = Table()
        self.MyAppWindow.addTable(mytable)
        self.assertTrue(self.MyAppWindow.tableWidget, mytable)

    def testAddLog(self):
        myLog = LogWidget()
        self.MyAppWindow.addLog(myLog)
        self.assertTrue(self.MyAppWindow.logWidget, myLog)

    def testaddSemiAuto(self):
        mySemi = SemiAuto(semiAutoPath)
        self.MyAppWindow.addSemiAuto(mySemi)
        self.assertTrue(self.MyAppWindow.semiAutoWidget, mySemi)

    def testAddGraphWidget(self):
        myGraph = Graph()
        self.MyAppWindow.addGraph(myGraph)
        self.assertTrue(self.MyAppWindow.graphWidget, myGraph)

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
        self.MyAppWindow = self.MyApp.application_window

    def testAddVision(self):
        vis = VideoWidget(videoPath)
        self.MyAppWindow.add_vision(vis)
        self.assertTrue(self.MyAppWindow.vision_widget, vis)

    def testAddTable(self):
        mytable = Table()
        self.MyAppWindow.add_table(mytable)
        self.assertTrue(self.MyAppWindow.table_widget, mytable)

    def testAddLog(self):
        myLog = LogWidget()
        self.MyAppWindow.add_log(myLog)
        self.assertTrue(self.MyAppWindow.log_widget, myLog)

    def testaddSemiAuto(self):
        mySemi = SemiAuto(semiAutoPath)
        self.MyAppWindow.add_semi_auto(mySemi)
        self.assertTrue(self.MyAppWindow.semi_auto_widget, mySemi)

    def testAddGraphWidget(self):
        myGraph = Graph()
        self.MyAppWindow.add_graph(myGraph)
        self.assertTrue(self.MyAppWindow.graph_widget, myGraph)

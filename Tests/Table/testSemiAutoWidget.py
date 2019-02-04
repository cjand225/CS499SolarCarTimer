import sys, os, unittest, time, threading

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QSignalSpy
from PyQt5.QtGui import QBrush, QPalette

from SCTimeUtility.App.App import App
from SCTimeUtility.Table.Table import Table
from SCTimeUtility.Table.Car import Car
from SCTimeUtility.Table.SemiAuto import SemiAuto

sys.path.insert(0, os.path.abspath("SCTimeUtility"))


class TestSemiAutoWidget(unittest.TestCase):
    def setUp(self):
        self.app = QApplication(sys.argv)

    @staticmethod
    def createWidget():
        semiAutoWidget = SemiAuto(Table.semiAutoUIPath)
        semiAutoWidget.show()
        return semiAutoWidget

    @staticmethod
    def addCar(semiAutoWidget):
        testCar = Car(0, "University of Kentucky")
        semiAutoWidget.addCar(testCar)
        return testCar

    def testAddCar(self):
        semiAutoWidget = type(self).createWidget()
        testCar = type(self).addCar(semiAutoWidget)
        self.assertEqual(testCar, semiAutoWidget.cars[0])
        carLabel = semiAutoWidget.buttonsLayout.itemAtPosition(0, SemiAuto.labelColumn).widget()
        self.assertEqual(testCar.carOrg,
                         semiAutoWidget.buttonsLayout.itemAtPosition(0, SemiAuto.labelColumn).widget().text())
        semiAutoWidget.close()

    def testSetCar(self):
        newCar = Car(1, "Foboar")
        semiAutoWidget = type(self).createWidget()
        type(self).addCar(semiAutoWidget)
        semiAutoWidget.setCar(0, newCar)
        self.assertEqual(newCar, semiAutoWidget.cars[0])
        self.assertEqual(newCar.carOrg,
                         semiAutoWidget.buttonsLayout.itemAtPosition(0, SemiAuto.labelColumn).widget().text())
        semiAutoWidget.close()

    def testDeleteCar(self):
        newCars = [Car(1, "Foo"), Car(2, "Baz")]
        semiAutoWidget = type(self).createWidget()
        type(self).addCar(semiAutoWidget)
        for newCar in newCars:
            semiAutoWidget.addCar(newCar)
        semiAutoWidget.deleteCar(newCars[0])
        self.assertEqual(newCars[1], semiAutoWidget.cars[1])
        self.assertEqual(newCars[1].carOrg,
                         semiAutoWidget.buttonsLayout.itemAtPosition(1, SemiAuto.labelColumn).widget().text())
        semiAutoWidget.deleteCarAtIndex(0)
        self.assertEqual(newCars[1], semiAutoWidget.cars[0])
        self.assertEqual(newCars[1].carOrg,
                         semiAutoWidget.buttonsLayout.itemAtPosition(0, SemiAuto.labelColumn).widget().text())
        semiAutoWidget.close()

    def testRecordTime(self):
        semiAutoWidget = type(self).createWidget()
        testCar = type(self).addCar(semiAutoWidget)
        spy = QSignalSpy(semiAutoWidget.carRecord)
        semiAutoWidget.clickRecord(0)
        self.assertTrue(spy.wait(250))
        self.assertEqual(len(spy), 1)
        firstClick = spy[0]
        self.assertEqual(firstClick[0], testCar)
        self.assertEqual(firstClick[1], 0)
        semiAutoWidget.close()

    def testEnableLapPrediction(self):
        semiAutoWidget = type(self).createWidget()
        testCar = type(self).addCar(semiAutoWidget)
        spy = QSignalSpy(semiAutoWidget.predictClicked)
        semiAutoWidget.clickPredict(0)
        self.assertTrue(spy.wait(250))
        self.assertEqual(len(spy), 1)
        firstClick = spy[0]
        self.assertEqual(firstClick[0], testCar)
        self.assertTrue(firstClick[1])
        self.assertEqual(firstClick[2], 0)
        del spy[0]
        semiAutoWidget.clickPredict(0)
        self.assertTrue(spy.wait(250))
        self.assertEqual(len(spy), 1)
        firstClick = spy[0]
        self.assertFalse(firstClick[1])

    def testShowPredict(self):
        palette = QPalette()
        semiAutoWidget = type(self).createWidget()
        testCar = type(self).addCar(semiAutoWidget)
        carButton = semiAutoWidget.buttonsLayout.itemAtPosition(0, SemiAuto.buttonColumn).widget()
        semiAutoWidget.showPredictAtIndex(0)
        self.assertEqual(carButton.palette().color(carButton.backgroundRole()), SemiAuto.predictColor)
        semiAutoWidget.clearPredictAtIndex(0)
        self.assertEqual(carButton.palette().color(carButton.backgroundRole()),
                         palette.color(carButton.backgroundRole()))
        semiAutoWidget.showPredict(testCar)
        self.assertEqual(carButton.palette().color(carButton.backgroundRole()), SemiAuto.predictColor)
        semiAutoWidget.clearPredict(testCar)
        self.assertEqual(carButton.palette().color(carButton.backgroundRole()),
                         palette.color(carButton.backgroundRole()))

    def tearDown(self):
        self.app.quit()

import sys, unittest

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtTest import QSignalSpy

from SCTimeUtility.App.App import App
from SCTimeUtility.Table.AddCarDialog import AddCarDialog
from SCTimeUtility.Table.Table import Table


class TestAddCarDialog(unittest.TestCase):
    def setUp(self):
        self.app = QApplication(sys.argv)

    @staticmethod
    def createWidget():
        addCarDialog = AddCarDialog(Table.addCarDialogUIPath)
        addCarDialog.show()
        return addCarDialog

    def invalidCheck(self, addCarDialog):
        spy = QSignalSpy(addCarDialog.finished)
        addCarDialog.buttonBox.buttons()[0].animateClick()
        self.assertFalse(spy.wait(250))
        self.assertEqual(len(spy), 0)
        self.assertTrue(addCarDialog.validationError.isVisible())
        addCarDialog.validationError.close()
        addCarDialog.buttonBox.buttons()[1].animateClick()
        self.assertTrue(spy.wait(250))
        self.assertEqual(len(spy), 1)
        finishResult = spy[0]
        self.assertEqual(finishResult[0], QDialog.Rejected)

    def testValidData(self):
        teamName = "University of Kentucky"
        teamNumber = 3
        addCarDialog = type(self).createWidget()
        addCarDialog.teamNameEdit.insert(teamName)
        addCarDialog.carNumberEdit.insert(str(teamNumber))
        spy = QSignalSpy(addCarDialog.finished)
        addCarDialog.buttonBox.buttons()[0].animateClick()
        self.assertTrue(spy.wait(250))
        self.assertEqual(len(spy), 1)
        finishResult = spy[0]
        self.assertEqual(finishResult[0], QDialog.Accepted)
        self.assertEqual(addCarDialog.teamName, teamName)
        self.assertEqual(addCarDialog.carNumber, teamNumber)

    def testInvalidCarNumber(self):
        teamName = "University of Kentucky"
        teamNumber = "foobar"
        addCarDialog = type(self).createWidget()
        addCarDialog.teamNameEdit.insert(teamName)
        addCarDialog.carNumberEdit.insert(teamNumber)
        self.invalidCheck(addCarDialog)
        self.assertEqual(addCarDialog.teamName, teamName)
        self.assertEqual(addCarDialog.carNumber, None)

    def testInvalidTeamName(self):
        teamNumber = 3
        addCarDialog = type(self).createWidget()
        addCarDialog.carNumberEdit.insert(str(teamNumber))
        self.invalidCheck(addCarDialog)
        self.assertEqual(addCarDialog.teamName, "")
        self.assertEqual(addCarDialog.carNumber, teamNumber)

    def tearDown(self):
        self.app.quit()

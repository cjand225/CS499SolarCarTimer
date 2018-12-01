import sys, os, unittest, time

sys.path.insert(0, os.path.abspath("src"))
from PyQt5.Qt import QApplication
from PyQt5.QtTest import QSignalSpy
from tests.table.ElidedLabelTestWidget import ElidedLabelTestWidget


class TestElidedLabel(unittest.TestCase):
    def setUp(self):
        self.app = QApplication(sys.argv)
        self.labelWidget = ElidedLabelTestWidget()
        self.labelWidget.show()

    def testElision(self):
        # Test that the ElidedLabel elides only when necessary.
        shortString = "a"
        longString = "a" * 100
        self.assertFalse(self.labelWidget.label.elided)
        self.labelWidget.label.setText(longString)
        # Calling paintEvent directly causes Qt to complain, but
        # it seems to work.
        # Should try to implement with QWaitCondition and
        # QThread later using an elisionChanged signal.
        self.labelWidget.label.paintEvent(None)
        self.assertTrue(self.labelWidget.label.elided)
        self.labelWidget.label.setText(shortString)
        self.labelWidget.label.paintEvent(None)
        self.assertFalse(self.labelWidget.label.elided)

    def tearDown(self):
        self.app.quit()

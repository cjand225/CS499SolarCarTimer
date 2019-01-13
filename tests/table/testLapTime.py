import unittest, math
from SCTimeUtility.table.LapTime import LapTime


class testLapTime(unittest.TestCase):

    def setUp(self):
        self.default_time = 0

    def testFloat(self):
        myLap = LapTime(3.1459)
        myfloat = float(myLap)
        self.assertEqual(myfloat, 3.1459)

    def testInt(self):
        myLap = LapTime(3.1459)
        myInt = int(myLap)
        self.assertEqual(myInt, 3)

    def testSub(self):
        myLap = LapTime(3.1459)
        sLap = LapTime(4.5232)

        timeDiff = myLap - sLap
        self.assertEqual(timeDiff, int((3.1459 - 4.532)))

    def testStr(self):
        myLap = LapTime(3.1459)
        stringVal = str(myLap)
        self.assertEqual("3", stringVal)

    def testGetElapsed(self):
        myLap = LapTime(3.1459)
        elap = myLap.getElapsed()
        self.assertEqual(3, elap)

    def testSetElasped(self):
        myLap = LapTime(3.1459)
        nVal = 3204
        myLap.setElapsed(nVal)
        self.assertEqual(nVal, myLap.getElapsed())
        nVal = 32.04
        myLap.setElapsed(nVal)
        self.assertEqual(int(nVal), myLap.getElapsed())

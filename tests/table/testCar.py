import unittest
import sys
import re

from src.table.Car import Car

class testCar(unittest.TestCase):

    def setUp(self):
        #self.car = Car(0)
        self.CorrectString = "University of Kentucky"

    def testCreateNormal(self):
        myCar = Car(1, "University of Kentucky", 23)
        self.assertTrue(myCar.ID == 1 )
        self.assertEqual(myCar.OrgName , self.CorrectString )
        self.assertTrue(myCar.CarNum == 23)

    def testaddTime(self):
        myCar = Car(1, "University of Kentucky", 23)
        myCar.addLapTime(1, 2, 3, 32)
        firstLap = myCar.LapList[0]

        #check if all lap data is correct within the list
        self.assertEqual(firstLap[0], 0)
        self.assertEqual(firstLap[1], 1)
        self.assertEqual(firstLap[2], 2)
        self.assertEqual(firstLap[3], 3)
        self.assertEqual(firstLap[4], 32)

    def testAddMultipleLaps(self):
        myCar = Car(1, "University of Kentucky", 23)
        myCar.addLapTime(2, 3, 4, 5)
        myCar.addLapTime(6, 7, 8, 9)
        firstLap = myCar.LapList[0]
        secondLap = myCar.LapList[1]
        #check if both laps match the ones in the list
        self.assertEqual(secondLap[0], 1)
        self.assertEqual(firstLap[0], 0)
        self.assertEqual(firstLap, myCar.LapList[0])
        self.assertEqual(secondLap, myCar.LapList[1])

    def testGetLap(self):
        myCar = Car(1, "University of Kentucky", 23)
        myCar.addLapTime(2, 3, 4, 5)
        myCar.addLapTime(6, 7, 8, 9)
        firstLap = myCar.LapList[0]
        myCar.editLapTime(0, 1, 1, 1, 1)
        firstLapCopy = myCar.getLapByID(0)
        self.assertNotEqual(firstLap, firstLapCopy)

    def testRemoveLap(self):
        myCar = Car(1, "University of Kentucky", 23)
        myCar.addLapTime(2, 3, 4, 5)
        myCar.addLapTime(6, 7, 8, 9)
        secondLap = myCar.LapList[1]
        myCar.removeLapTime(1)
        self.assertNotEqual(secondLap, myCar.LapList[1])

    def testRemoveMultipleLaps(self):
        myCar = Car(1, "University of Kentucky", 23)
        myCar.addLapTime(2, 3, 4, 5)
        myCar.addLapTime(6, 7, 8, 9)
        firstLap = myCar.LapList[0]
        secondLap = myCar.LapList[1]
        myCar.removeLapTime(0)
        myCar.removeLapTime(1)
        self.assertNotEqual(firstLap, myCar.LapList[0])
        self.assertNotEqual(secondLap, myCar.LapList[1])

    def testGetCarID(self):
        myCar = Car(1, "University of Kentucky", 23)
        myID = myCar.getCarID()
        self.assertEqual(myID, 1)

    def testGetCarOrg(self):
        myCar = Car(1, "University of Kentucky", 23)
        myOrg = myCar.getOrg()
        self.assertEqual(myOrg, "University of Kentucky")

    def testGetCarNum(self):
        myCar = Car(1, "University of Kentucky", 23)
        myCarNum = myCar.getCarNum()
        self.assertEqual(myCarNum, 23)

    def testIDChanged(self):
        myCar = Car(1, "University of Kentucky", 23)
        myCar.editID(0)
        self.assertEqual(myCar.getCarID(), 0)

    def testLapCount(self):
        myCar = Car(1, "University of Kentucky", 23)
        myCar.addLapTime(2, 3, 4, 5)
        myCar.addLapTime(6, 7, 8, 9)
        self.assertEqual(myCar.getLapCount(), 2)



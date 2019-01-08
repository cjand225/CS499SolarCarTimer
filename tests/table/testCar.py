import unittest, sys, time, re, random

from SCTimeUtility.system.TimeReferences import LapTime
from SCTimeUtility.table.Car import Car


class testCar(unittest.TestCase):

    def setUp(self):
        self.RegExpID = "^([0-9][0-9]{0,2}|1000)$"
        self.RegExpTeamName = "^[a-zA-Z]+(?:[\s-][a-zA-Z]+)*$"
        self.RegExpCarNum = "^(?:500|[1-9]?[0-9])$"

    def testCreateNormal(self):
        myCar = Car(1, "University of Kentucky", 23)
        self.assertRegex(str(myCar.ID), self.RegExpID)
        self.assertRegex(str(myCar.CarNum), self.RegExpCarNum)
        self.assertRegex(str(myCar.TeamName), self.RegExpTeamName)

    def testCreateMalformed(self):
        myCar = Car("A", "hi", 23)
        self.assertNotEqual(myCar.getID(), "A")
        self.assertNotEqual(myCar.ID, "A")

    def testSetCarID(self):
        myCar = Car(1, "University of Kentucky", 23)
        myCar.setID(2)
        self.assertEqual(myCar.ID, 2)

    def testSeedValue(self):
        myCar = Car(1, "University of Kentucky", 23)
        seedVal = time.time()
        myCar.setSeedValue(seedVal)
        self.assertIsNotNone(myCar.getSeedValue())
        self.assertIsNotNone(myCar.SeedValue)
        self.assertEqual(myCar.SeedValue, myCar.getSeedValue())
        self.assertEqual(myCar.getSeedValue(), seedVal)
        self.assertEqual(myCar.SeedValue, seedVal)

    def testaddTime(self):
        myCar = Car(1, "University of Kentucky", 23)
        seedTime = time.time()
        testTime = time.time()
        myCar.setSeedValue(seedTime)
        myCar.addLapManually(testTime)
        firstLap = LapTime(testTime).getElapsed()
        self.assertEqual(firstLap, myCar.getLap(1).getElapsed())

    def testAddMultipleLaps(self):
        numOfLaps = 500
        myCar = Car(1, "University of Kentucky", 23)
        myCar.setSeedValue(time.time())
        lapList = []
        for x in range(0, numOfLaps):
            timeAdd = time.time()
            lapList.append(LapTime(timeAdd))
            myCar.addLapManually(timeAdd)
        # check if all laps added
        self.assertEqual(numOfLaps, myCar.getLapCount())
        # check for accuracy of each lap
        for x in range(0, numOfLaps - 1):
            self.assertEqual(lapList[x].getElapsed(), myCar.getLap(x + 1).getElapsed())

    def testGetLap(self):
        numOfLaps = 500
        myCar = Car(1, "University of Kentucky", 23)
        myCar.setSeedValue(time.time())
        lapList = []
        for x in range(0, numOfLaps):
            timeAdd = time.time()
            lapList.append(LapTime(timeAdd))
            myCar.addLapTime(timeAdd)
        randomLap = random.randint(0, 499)
        self.assertEqual(myCar.getLap(randomLap), myCar.LapList[randomLap])

    def testRemoveLap(self):
        numOfLaps = 500
        myCar = Car(1, "University of Kentucky", 23)
        myCar.setSeedValue(time.time())
        lapList = []
        for x in range(0, numOfLaps):
            lapList.append(time.time())
            myCar.addLapTime(lapList[x])
        # only first 5, since list index would be Out of range after removal
        lapRemoved = random.randint(0, 5)
        self.assertNotEqual(lapList[lapRemoved], myCar.LapList[lapRemoved])

    def testRemoveMultipleLaps(self):
        numOfLaps = 50
        myCar = Car(1, "University of Kentucky", 23)
        myCar.setSeedValue(time.time())
        lapList = []
        removalList = []

    def testGetCarID(self):
        myCar = Car(1, "University of Kentucky", 23)
        myID = myCar.getID()
        self.assertEqual(myID, 1)

    def testGetCarTeamName(self):
        myCar = Car(1, "University of Kentucky", 23)
        myOrg = myCar.getTeam()
        self.assertEqual(myOrg, "University of Kentucky")

    def testGetCarNum(self):
        myCar = Car(1, "University of Kentucky", 23)
        myCarNum = myCar.getCarNum()
        self.assertEqual(myCarNum, 23)

    def testLapCount(self):
        myCar = Car(1, "University of Kentucky", 23)
        myCar.setSeedValue(time.time())
        for x in range(0, 4):
            myCar.addLapTime(time.time())
        self.assertEqual(myCar.getLapCount(), 4)

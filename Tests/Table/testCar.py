import unittest, sys, math, datetime
from PyQt5.QtTest import QSignalSpy

from SCTimeUtility.Table.LapTime import LapTime
from SCTimeUtility.Table.Car import Car
from Tests.DataGen.DataGeneration import *


class testCar(unittest.TestCase):

    def setUp(self):
        self.RegExpID = "^([0-9][0-9]{0,2}|1000)$"
        self.RegExpTeamName = "^[a-zA-Z]+(?:[\s-][a-zA-Z]+)*$"
        self.RegExpCarNum = "^(?:500|[1-9]?[0-9])$"
        self.validTestString = "University of Kentucky"
        self.validCarNumber = 23
        self.numOfLaps = 300
        self.editNum = 100

    def testCreateNormal(self):
        myCar = Car(1, self.validTestString, self.validCarNumber)
        self.assertRegex(str(myCar.ID), self.RegExpID)
        self.assertRegex(str(myCar.CarNum), self.RegExpCarNum)
        self.assertRegex(str(myCar.TeamName), self.RegExpTeamName)
        self.assertEqual(myCar.ID, 1)
        self.assertEqual(myCar.TeamName, self.validTestString)
        self.assertEqual(myCar.CarNum, self.validCarNumber)

    def testCreateMalformed(self):
        self.assertRaises(Exception, Car, "A", "hi", self.validCarNumber)
        self.assertRaises(Exception, Car, "hi", "A", "as")
        self.assertRaises(Exception, Car, 1, 12, "23")
        self.assertRaises(Exception, Car, None, None, None)
        self.assertRaises(Exception, Car)

    def testSetCarID(self):
        myCar = Car(1, self.validTestString, self.validCarNumber)
        myCar.setID(2)
        self.assertEqual(myCar.ID, 2)

    def testSeedValue(self):
        myCar = Car(1, self.validTestString, self.validCarNumber)
        seedVal = time.time()
        myCar.setSeedValue(seedVal)
        self.assertIsNotNone(myCar.getSeedValue())
        self.assertIsNotNone(myCar.SeedValue)
        self.assertEqual(myCar.SeedValue, myCar.getSeedValue())
        self.assertEqual(myCar.getSeedValue(), seedVal)
        self.assertEqual(myCar.SeedValue, seedVal)

    def testaddTime(self):
        myCar = Car(1, self.validTestString, self.validCarNumber)
        seedTime = time.time()
        testTime = time.time()
        myCar.setSeedValue(seedTime)
        myCar.addLapTime(testTime)
        firstLap = LapTime(testTime).getElapsed()
        self.assertEqual(firstLap, myCar.getLap(1).getElapsed())

    def testAddMultipleLaps(self):
        myCar = Car(1, self.validTestString, self.validCarNumber)
        myCar.setSeedValue(time.time())
        lapList = []
        for x in range(0, self.numOfLaps):
            timeAdd = time.time()
            lapList.append(LapTime(timeAdd))
            myCar.addLapManually(timeAdd)
        # check if all laps added - account for seed value in first index
        self.assertEqual(self.numOfLaps, myCar.getLapCount() - 1)
        # check for accuracy of each lap - account for seed value
        for x in range(0, self.numOfLaps - 1):
            self.assertEqual(lapList[x].getElapsed(), myCar.getLap(x + 1).getElapsed())

    def testGetLap(self):
        myCar = Car(1, self.validTestString, self.validCarNumber)
        myCar.setSeedValue(time.time())
        lapList = []
        for x in range(0, self.numOfLaps):
            timeAdd = time.time()
            lapList.append(LapTime(timeAdd))
            myCar.addLapTime(timeAdd)
        randomLap = random.randint(0, self.numOfLaps - 1)
        self.assertEqual(myCar.getLap(randomLap), myCar.LapList[randomLap])

    def testRemoveLap(self):
        myCar = Car(1, self.validTestString, self.validCarNumber)
        QtSpyBot = QSignalSpy(myCar.lapChanged)
        myCar.setSeedValue(time.time())
        lapList = generateLapData(self.numOfLaps)
        for x in range(0, self.numOfLaps):
            myCar.addLapTime(lapList[x])
        # only first 5, since list index would be Out of range after removal
        lapRemoved = random.randint(0, 5)
        # 501 signals emitted because seedvalue call emits signal as well
        self.assertEqual(len(lapList) + 1, len(QtSpyBot))
        self.assertNotEqual(lapList[lapRemoved], myCar.LapList[lapRemoved].elapsedTime)

    def testRemoveMultipleLaps(self):
        myCar = Car(1, self.validTestString, self.validCarNumber)
        myCar.setSeedValue(time.time())
        lapList = generateLapData(self.numOfLaps)
        for x in range(0, self.numOfLaps):
            myCar.addLapTime(lapList[x])

        for x in range(0, self.numOfLaps - 1):
            # account for amount of laps,
            randLap = random.randint(0, myCar.getLastLapIndex())
            myCar.removeLapTime(randLap)
            self.assertEqual(self.numOfLaps + 1, myCar.getLapCount())
            self.assertEqual(0, myCar.getLap(randLap).elapsedTime)

    def testGetCarID(self):
        myCar = Car(1, self.validTestString, self.validCarNumber)
        myID = myCar.getID()
        self.assertEqual(myID, 1)

    def testGetCarTeamName(self):
        myCar = Car(1, self.validTestString, self.validCarNumber)
        myOrg = myCar.getTeam()
        self.assertEqual(myOrg, self.validTestString)

    def testGetCarNum(self):
        myCar = Car(1, self.validTestString, self.validCarNumber)
        myCarNum = myCar.getCarNum()
        self.assertEqual(myCarNum, self.validCarNumber)

    def testLapCount(self):
        myCar = Car(1, self.validTestString, self.validCarNumber)
        myCar.setSeedValue(time.time())
        for x in range(0, self.numOfLaps):
            myCar.addLapTime(time.time())
        # check if laps added is same - account for seedvalue offset
        self.assertEqual(myCar.getLapCount(), self.numOfLaps + 1)

    def testGetTotalElapsedTime(self):
        myCar = Car(1, self.validTestString, self.validCarNumber)
        myCar.setSeedValue(time.time())
        randIndex = random.randint(0, self.numOfLaps - 1)
        lapData = generateLapData(self.numOfLaps)
        for lap in lapData:
            myCar.addLapTime(LapTime(datetime.timedelta(seconds=lap)))

        allLaps = myCar.LapList[1:randIndex]
        totalElapsed = sum([lap for lap in allLaps])
        totalFromCar = myCar.getTotalElapsedTime(randIndex)
        self.assertEqual(totalElapsed, totalFromCar)

    def testGetFastestLap(self):
        myCar = Car(1, self.validTestString, self.validCarNumber)
        myCar.setSeedValue(time.time())
        lapData = generateLapData(self.numOfLaps)
        for lap in lapData:
            myCar.addLapTime(lap)
        fastest = min([LapTime(lap).getElapsed() for lap in lapData])
        self.assertEqual(fastest, myCar.getFastestLap())

    def testEditLap(self):
        myCar = Car(1, self.validTestString, self.validCarNumber)
        myCar.setSeedValue(time.time())
        lapData = generateLapData(self.numOfLaps)
        # let 5 seconds pass to generate new times
        editLapData = generateLapData(self.numOfLaps)
        editIndices = []

        # add laps to car
        for x in range(0, self.numOfLaps - 1):
            myCar.addLapTime(lapData[x])
            randIndex = random.randint(0, self.numOfLaps - 1)
            if randIndex not in editIndices:
                editIndices.append(randIndex)

        for x in range(1, len(editIndices) - 1):
            orgLapBelow = editIndices[x] + 1
            orgData = myCar.LapList[editIndices[x]].elapsedTime
            edit = editLapData[x]

            if orgLapBelow in range(0, len(myCar.LapList) - 1):
                orgDataBelow = myCar.LapList[orgLapBelow].elapsedTime
                totalTime = orgData + orgDataBelow
                myCar.editLapTime(editIndices[x], edit)
                editBelow = totalTime - edit

                self.assertEqual(myCar.LapList[editIndices[x]].elapsedTime, edit)
                self.assertEqual(myCar.LapList[editIndices[x] + 1].elapsedTime, LapTime(editBelow).elapsedTime)
                self.assertNotEqual(myCar.LapList[editIndices[x]].elapsedTime, orgData)

            else:
                myCar.editLapTime(editIndices[x], edit)
                self.assertEqual(myCar.LapList[editIndices[x]].elapsedTime, edit)

    def testIndexExists(self):
        myCar = Car(1, self.validTestString, self.validCarNumber)
        myCar.setSeedValue(time.time())
        lapData = generateLapData(self.numOfLaps)
        # let 5 seconds pass to generate new times
        editLapData = generateLapData(self.numOfLaps)

        # add laps to car
        for x in range(0, self.numOfLaps - 1):
            myCar.addLapTime(lapData[x])

        for x in range(0, self.numOfLaps - 1):
            self.assertTrue(myCar.indexExists(x))
        self.assertFalse(myCar.indexExists(-1))
        self.assertFalse(myCar.indexExists(self.numOfLaps))

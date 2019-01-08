import re, unittest, random, string

from SCTimeUtility.table.Car import Car
from SCTimeUtility.table.CarStorage import CarStorage

from tests.dataGen.testFunctions import randomWord


class testCarStorage(unittest.TestCase):

    def setUp(self):
        self.maxCars = 500
        self.carListData = []
        self.randTeamName = ''

        for x in range(0, self.maxCars):
            clist = []
            wordLength = random.randint(0, 20)
            randLetters = randomWord(wordLength)
            if self.randTeamName == '':
                self.randTeamName = randLetters
            clist.append(randLetters)
            clist.append(random.randint(0, 500))
            self.carListData.append(clist)

    def testCreateCarStorage(self):
        myStore = CarStorage()
        self.assertIsInstance(myStore, CarStorage)

    def testCreateCar(self):
        myStore = CarStorage()
        myStore.createCar(self.carListData[0][0], self.carListData[0][1])
        self.assertIsInstance(myStore.storageList[0], Car)
        self.assertEqual(self.carListData[0], [myStore.storageList[0].TeamName, myStore.storageList[0].CarNum])

    def testCreateCars(self):
        myStore = CarStorage()
        myStore.createCars(self.carListData)
        self.assertEqual(self.maxCars, myStore.getCarAmount())
        for x in range(0, self.maxCars):
            self.assertEqual(self.carListData[x], [myStore.storageList[x].TeamName, myStore.storageList[x].CarNum])

    def testRemoveCar(self):
        myStore = CarStorage()
        myStore.createCars(self.carListData)
        testCar = myStore.getCarByID(0)
        reIndexedCar = myStore.getCarByID(1)
        myStore.removeCar(0)
        self.assertNotEqual(myStore.storageList[0], testCar)
        self.assertEqual(myStore.storageList[0], reIndexedCar)

    def testgetCarByCarNum(self):
        myStore = CarStorage()
        myStore.createCars(self.carListData)
        randCar = random.randint(0, len(self.carListData) - 2)
        self.assertEqual(myStore.getCarByNum(randCar).CarNum, randCar)

    def testgetCarByID(self):
        myStore = CarStorage()
        myStore.createCars(self.carListData)
        myCar = myStore.getCarByID(1)
        self.assertIsInstance(myStore.storageList[1].ID, int)
        self.assertEqual(myStore.storageList[1].ID, myCar.ID)

    def testgetCarByOrg(self):
        myStore = CarStorage()
        myStore.createCars(self.carListData)
        for x in range(0, self.maxCars):
            self.assertIsInstance(myStore.getCarByTeamName(self.randTeamName).TeamName, str)
            self.assertEqual(myStore.getCarByTeamName(self.randTeamName).TeamName, self.randTeamName)

    def testreindex(self):
        myStore = CarStorage()
        myStore.createCars(self.carListData)
        firstCar = myStore.getCarByID(1)
        secondCar = myStore.getCarByID(2)
        myStore.removeCar(firstCar.ID)
        myStore.reindexStorage(firstCar.ID)
        self.assertNotEqual(firstCar, myStore.getCarByID(1))
        self.assertEqual(secondCar, myStore.storageList[1])

    def testAppendLapTime(self):
        myStore = CarStorage()
        myStore.addCar(myStore.getLatestCarID(), 'University of Kentucky', 45)
        myCar = myStore.getCarByID(0)
        CarLap = myCar.getLapByID(0)
        self.assertEqual(CarLap[1], 1)
        self.assertEqual(CarLap[2], 5)
        self.assertEqual(CarLap[3], 3)
        self.assertEqual(CarLap[4], 2)

    def testEditLaptime(self):
        myStore = CarStorage()
        myStore.addCar(myStore.getLatestCarID(), 'University of Kentucky', 45)
        myCar = myStore.getCarByID(0)
        myCar.addLapTime(1, 1, 1, 1)
        myStore.editLapTime(0, 0, 23, 34, 32, 23)
        LapOne = myCar.LapList[0]
        self.assertEqual(LapOne[1], 23)
        self.assertEqual(LapOne[2], 34)
        self.assertEqual(LapOne[3], 32)
        self.assertEqual(LapOne[4], 23)

    def testGetCopyStorage(self):
        myStore = CarStorage()
        myStore.addCar(myStore.getLatestCarID(), 'University of Kentucky', 45)
        newList = myStore.getCarListCopy()
        self.assertEqual(newList, myStore.storageList)
        self.assertEqual(newList[0], myStore.storageList[0])

    def testRemoveLap(self):
        myStore = CarStorage()
        myStore.addCar(myStore.getLatestCarID(), 'University of Kentucky', 45)
        myStore.addCar(myStore.getLatestCarID(), 'University of y', 42)
        myCar = myStore.getCarByID(0)
        myCar.addLapTime(1, 1, 1, 1)
        myStore.removeLapTime(0, 0)
        LapOne = myCar.LapList[0]
        self.assertEqual(LapOne[1], 0)
        self.assertEqual(LapOne[2], 0)
        self.assertEqual(LapOne[3], 0)
        self.assertEqual(LapOne[4], 0)

    def testGetOrgNames(self):
        myStore = CarStorage()
        myStore.addCar(myStore.getLatestCarID(), 'University of Kentucky', 45)
        myStore.addCar(myStore.getLatestCarID(), 'University of y', 42)
        newlist = []
        newlist.append(myStore.getCarByID(0).getTeam())
        newlist.append(myStore.getCarByID(1).getTeam())
        self.assertEqual(newlist, myStore.getCarNamesList())

    def testGetCarAmount(self):
        myStore = CarStorage()
        myStore.addCar(myStore.getLatestCarID(), 'University of Kentucky', 45)
        myStore.addCar(myStore.getLatestCarID(), 'University of y', 42)
        self.assertEqual(myStore.getCarAmount(), 2)

    def testGetHighestLapCount(self):
        myStore = CarStorage()
        myStore.addCar(myStore.getLatestCarID(), 'University of Kentucky', 45)
        myStore.addCar(myStore.getLatestCarID(), 'University of y', 42)
        myStore.appendLapTime(0, 1, 1, 1, 1)
        myStore.appendLapTime(0, 2, 3, 4, 5)
        myStore.appendLapTime(1, 3, 4, 6, 7)

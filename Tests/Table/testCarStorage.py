import re, unittest, random, string, time, copy

from SCTimeUtility.Table.Car import Car
from SCTimeUtility.Table.CarStorage import CarStorage
from SCTimeUtility.Table.LapTime import LapTime

from Tests.DataGen.DataGeneration import generateLapData, generateCarData, generateCarInfo, populateStorage


class testCarStorage(unittest.TestCase):

    def setUp(self):
        self.maxCars = 300
        self.maxLaps = 300
        self.carListData = generateCarInfo(self.maxCars)

    def testCreateCarStorage(self):
        myStore = CarStorage()
        self.assertIsInstance(myStore, CarStorage)

    def testCreateCar(self):
        myStore = CarStorage()
        carListData = generateCarData(self.maxCars)
        carToCreate = [carListData[0][1], carListData[0][2]]
        myStore.createCar(carToCreate[1], carToCreate[0])
        self.assertIsInstance(myStore.storageList[0], Car)
        self.assertEqual(carToCreate, [myStore.storageList[0].TeamName, myStore.storageList[0].CarNum])

    def testCreateCars(self):
        myStore = CarStorage()
        carListData = generateCarInfo(self.maxCars)
        myStore.createCars(carListData)
        self.assertEqual(self.maxCars, myStore.getCarCount())
        for x in range(0, self.maxCars):
            self.assertEqual(carListData[x], [myStore.storageList[x].TeamName, myStore.storageList[x].CarNum])

    def testRemoveCar(self):
        myStore = CarStorage()
        carListData = generateCarInfo(self.maxCars)
        myStore.createCars(carListData)
        testCar = myStore.getCarByID(0)
        reIndexedCar = myStore.getCarByID(1)
        myStore.removeCar(0)
        self.assertNotEqual(myStore.storageList[0], testCar)
        self.assertEqual(myStore.storageList[0], reIndexedCar)

    def testgetCarByID(self):
        myStore = CarStorage()
        carListData = generateCarInfo(self.maxCars)
        myStore.createCars(carListData)
        myCar = myStore.getCarByID(1)
        self.assertIsInstance(myStore.storageList[1].ID, int)
        self.assertEqual(myStore.storageList[1].ID, myCar.ID)

    def testgetCarByCarNum(self):
        myStore = CarStorage()
        carListData = generateCarInfo(self.maxCars)
        myStore.createCars(carListData)
        for x in range(0, self.maxCars - 1):
            randCarData = random.randint(0, len(carListData) - 1)
            randCar = carListData[randCarData][1]
            self.assertEqual(myStore.getCarByNum(randCar).CarNum, randCar)

    def testgetCarByTeamName(self):
        myStore = CarStorage()
        carListData = generateCarInfo(self.maxCars)
        myStore.createCars(carListData)
        for x in range(0, self.maxCars):
            randCarData = random.randint(0, len(carListData) - 1)
            randCar = carListData[randCarData][0]
            self.assertEqual(myStore.getCarByTeamName(randCar).TeamName, randCar)

    def testReIndex(self):
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
        myStore.createCar(45, 'University of Kentucky')
        myCar = myStore.storageList[0]
        myCar.setSeedValue(time.time())
        lapData = generateLapData(self.maxLaps)

        for lapIndex in range(0, len(lapData)):
            myCar.addLapTime(lapData[lapIndex])
            fakeLap = LapTime(lapData[lapIndex])
            self.assertEqual(fakeLap.getElapsed(), myCar.lapList[lapIndex + 1].getElapsed())

    def testEditLaptime(self):
        myStore = CarStorage()
        myStore.createCar(45, 'University of Kentucky')
        myStore.createCar(4, 'University of Ken')
        myCar = myStore.storageList[0]
        myCar.setSeedValue(time.time())
        lapData = generateLapData(self.maxLaps)

        # populate data
        for car in myStore.storageList:
            for lapIndex in range(0, len(lapData)):
                car.addLapTime(lapData[lapIndex])
                randCar = int(random.randrange(0, len(myStore.storageList) - 1))
                randLap = int(random.randrange(1, len(lapData) - 1))

        # randomize and select car, verify it doesnt match original time and matches edit time

    def testGetCopyStorage(self):
        myStore = CarStorage()
        newCarData = generateCarInfo(self.maxCars)
        myStore.createCars(newCarData)

        # verify they're the same classes
        self.assertEqual(myStore.storageList.__class__, newCarData.__class__)
        # verify they don't share the same memory space and same for their objects
        self.assertNotEqual(myStore.storageList, newCarData)
        for x in range(0, len(myStore.storageList) - 1):
            self.assertNotEqual(myStore.storageList[x], newCarData[x])

    def testRemoveLap(self):
        myStore = CarStorage()
        carList = generateCarInfo(self.maxCars)
        myStore.createCars(carList)
        lapData = generateLapData(self.maxLaps)

        # populate data for each car
        for x in range(0, len(myStore.storageList) - 1):
            if myStore.storageList[x].SeedValue is None:
                myStore.storageList[x].setSeedValue(time.time())
            for lapIndex in range(0, len(lapData)):
                myStore.storageList[x].addLapTime(lapData[lapIndex])

        # pick a random lap each time, confirm its zero'd out
        for x in range(0, self.maxCars - 1):
            currCar = myStore.storageList[x]
            randLapIndex = random.randrange(1, len(currCar.lapList) - 1)
            myStore.storageList[x].removeLapTime(randLapIndex)
            self.assertEqual(myStore.storageList[x].getLapCount() - 1, self.maxLaps)
            self.assertEqual(myStore.storageList[x].lapList[randLapIndex].elapsedTime, 0)

    def testGetTeamNames(self):
        myStore = CarStorage()
        newCarData = generateCarInfo(self.maxCars)
        myStore.createCars(newCarData)

        for x in range(0, self.maxCars):
            randomCarIndex = int(random.randrange(0, self.maxCars - 1))
            self.assertIsNotNone(myStore.getCarByTeamName(newCarData[randomCarIndex][0]))
            self.assertEqual(myStore.getCarByTeamName(newCarData[randomCarIndex][0]).TeamName,
                             newCarData[randomCarIndex][0])

    def testGetCarCount(self):
        randomAmount = random.randrange(0, self.maxCars)
        for x in range(0, randomAmount):
            myStore = CarStorage()
            carListSize = random.randrange(0, self.maxCars)
            newCarData = generateCarInfo(carListSize)
            myStore.createCars(newCarData)
            self.assertEqual(myStore.getCarCount(), carListSize)

    def testGetHighestLapCount(self):
        myStore = CarStorage()
        newCarData = generateCarInfo(self.maxCars)
        lapData = generateLapData(self.maxLaps)
        myStore.createCars(newCarData)

        # add self.maxCars Amount of Cars, randomize how many laps are added, verify they match the amount selected
        highestLapAmount = 0
        for car in myStore.storageList:
            if car.SeedValue is None:
                car.setSeedValue(time.time())
            # pick a random amount of laps to add
            randLapAmount = random.randrange(0, len(lapData))
            for lap in range(0, randLapAmount):
                car.addLapTime(lapData[lap])
            # account for seed value
            self.assertEqual(car.getLapCount() - 1, randLapAmount)
            if car.getLapCount() > highestLapAmount:
                highestLapAmount = car.getLapCount()

        self.assertEqual(myStore.getHighestLapCount(), highestLapAmount)

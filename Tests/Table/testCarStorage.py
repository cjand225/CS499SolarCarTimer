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
        myStore.create_car(carToCreate[1], carToCreate[0])
        self.assertIsInstance(myStore.storage_list[0], Car)
        self.assertEqual(carToCreate, [myStore.storage_list[0].TeamName, myStore.storage_list[0].CarNum])

    def testCreateCars(self):
        myStore = CarStorage()
        carListData = generateCarInfo(self.maxCars)
        myStore.create_cars(carListData)
        self.assertEqual(self.maxCars, myStore.get_car_count())
        for x in range(0, self.maxCars):
            self.assertEqual(carListData[x], [myStore.storage_list[x].TeamName, myStore.storage_list[x].CarNum])

    def testRemoveCar(self):
        myStore = CarStorage()
        carListData = generateCarInfo(self.maxCars)
        myStore.create_cars(carListData)
        testCar = myStore.get_car_by_id(0)
        reIndexedCar = myStore.get_car_by_id(1)
        myStore.remove_car(0)
        self.assertNotEqual(myStore.storage_list[0], testCar)
        self.assertEqual(myStore.storage_list[0], reIndexedCar)

    def testgetCarByID(self):
        myStore = CarStorage()
        carListData = generateCarInfo(self.maxCars)
        myStore.create_cars(carListData)
        myCar = myStore.get_car_by_id(1)
        self.assertIsInstance(myStore.storage_list[1].ID, int)
        self.assertEqual(myStore.storage_list[1].ID, myCar.ID)

    def testgetCarByCarNum(self):
        myStore = CarStorage()
        carListData = generateCarInfo(self.maxCars)
        myStore.create_cars(carListData)
        for x in range(0, self.maxCars - 1):
            randCarData = random.randint(0, len(carListData) - 1)
            randCar = carListData[randCarData][1]
            self.assertEqual(myStore.get_car_by_car_number(randCar).CarNum, randCar)

    def testgetCarByTeamName(self):
        myStore = CarStorage()
        carListData = generateCarInfo(self.maxCars)
        myStore.create_cars(carListData)
        for x in range(0, self.maxCars):
            randCarData = random.randint(0, len(carListData) - 1)
            randCar = carListData[randCarData][0]
            self.assertEqual(myStore.get_car_by_team_name(randCar).TeamName, randCar)

    def testReIndex(self):
        myStore = CarStorage()
        myStore.create_cars(self.carListData)
        firstCar = myStore.get_car_by_id(1)
        secondCar = myStore.get_car_by_id(2)
        myStore.remove_car(firstCar.ID)
        myStore.sort_storage(firstCar.ID)
        self.assertNotEqual(firstCar, myStore.get_car_by_id(1))
        self.assertEqual(secondCar, myStore.storage_list[1])

    def testAppendLapTime(self):
        myStore = CarStorage()
        myStore.create_car(45, 'University of Kentucky')
        myCar = myStore.storage_list[0]
        myCar.set_seed_value(time.time())
        lapData = generateLapData(self.maxLaps)

        for lapIndex in range(0, len(lapData)):
            myCar.addLapTime(lapData[lapIndex])
            fakeLap = LapTime(lapData[lapIndex])
            self.assertEqual(fakeLap.get_elapsed(), myCar.lapList[lapIndex + 1].get_elapsed_time())

    def testEditLaptime(self):
        myStore = CarStorage()
        myStore.create_car(45, 'University of Kentucky')
        myStore.create_car(4, 'University of Ken')
        myCar = myStore.storage_list[0]
        myCar.set_seed_value(time.time())
        lapData = generateLapData(self.maxLaps)

        # populate data
        for car in myStore.storage_list:
            for lapIndex in range(0, len(lapData)):
                car.addLapTime(lapData[lapIndex])
                randCar = int(random.randrange(0, len(myStore.storage_list) - 1))
                randLap = int(random.randrange(1, len(lapData) - 1))

        # randomize and select car, verify it doesnt match original time and matches edit time

    def testGetCopyStorage(self):
        myStore = CarStorage()
        newCarData = generateCarInfo(self.maxCars)
        myStore.create_cars(newCarData)

        # verify they're the same classes
        self.assertEqual(myStore.storage_list.__class__, newCarData.__class__)
        # verify they don't share the same memory space and same for their objects
        self.assertNotEqual(myStore.storage_list, newCarData)
        for x in range(0, len(myStore.storage_list) - 1):
            self.assertNotEqual(myStore.storage_list[x], newCarData[x])

    def testRemoveLap(self):
        myStore = CarStorage()
        carList = generateCarInfo(self.maxCars)
        myStore.create_cars(carList)
        lapData = generateLapData(self.maxLaps)

        # populate data for each car
        for x in range(0, len(myStore.storage_list) - 1):
            if myStore.storage_list[x].SeedValue is None:
                myStore.storage_list[x].set_seed_value(time.time())
            for lapIndex in range(0, len(lapData)):
                myStore.storage_list[x].addLapTime(lapData[lapIndex])

        # pick a random lap each time, confirm its zero'd out
        for x in range(0, self.maxCars - 1):
            currCar = myStore.storage_list[x]
            randLapIndex = random.randrange(1, len(currCar.lapList) - 1)
            myStore.storage_list[x].remove_lap_time(randLapIndex)
            self.assertEqual(myStore.storage_list[x].getLapCount() - 1, self.maxLaps)
            self.assertEqual(myStore.storage_list[x].lapList[randLapIndex].elapsedTime, 0)

    def testGetTeamNames(self):
        myStore = CarStorage()
        newCarData = generateCarInfo(self.maxCars)
        myStore.create_cars(newCarData)

        for x in range(0, self.maxCars):
            randomCarIndex = int(random.randrange(0, self.maxCars - 1))
            self.assertIsNotNone(myStore.get_car_by_team_name(newCarData[randomCarIndex][0]))
            self.assertEqual(myStore.get_car_by_team_name(newCarData[randomCarIndex][0]).TeamName,
                             newCarData[randomCarIndex][0])

    def testGetCarCount(self):
        randomAmount = random.randrange(0, self.maxCars)
        for x in range(0, randomAmount):
            myStore = CarStorage()
            carListSize = random.randrange(0, self.maxCars)
            newCarData = generateCarInfo(carListSize)
            myStore.create_cars(newCarData)
            self.assertEqual(myStore.get_car_count(), carListSize)

    def testGetHighestLapCount(self):
        myStore = CarStorage()
        newCarData = generateCarInfo(self.maxCars)
        lapData = generateLapData(self.maxLaps)
        myStore.create_cars(newCarData)

        # add self.maxCars Amount of Cars, randomize how many laps are added, verify they match the amount selected
        highestLapAmount = 0
        for car in myStore.storage_list:
            if car.SeedValue is None:
                car.set_seed_value(time.time())
            # pick a random amount of laps to add
            randLapAmount = random.randrange(0, len(lapData))
            for lap in range(0, randLapAmount):
                car.addLapTime(lapData[lap])
            # account for seed value
            self.assertEqual(car.getLapCount() - 1, randLapAmount)
            if car.getLapCount() > highestLapAmount:
                highestLapAmount = car.getLapCount()

        self.assertEqual(myStore.get_highest_lap_count(), highestLapAmount)

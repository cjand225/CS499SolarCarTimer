from src.table.Car import Car
from src.table.CarStorage import CarStorage
import re
import unittest


class testCarStorage(unittest.TestCase):

    def testCreateCarStorage(self):
        myStore = CarStorage()
        self.assertIs(myStore.__class__, CarStorage)

    def testAddCar(self):
        myStore = CarStorage()
        myStore.addCar(myStore.getLatestCarID(), 'University of Kentucky', 45)
        testCar = myStore.storageList[0]
        self.assertEqual(myStore.storageList[0], testCar)

    def testRemoveCar(self):
        myStore = CarStorage()
        myStore.addCar(myStore.getLatestCarID(), 'University of Kentucky', 45)
        myStore.addCar(myStore.getLatestCarID(), 'University', 11)
        myStore.addCar(myStore.getLatestCarID(), 'University', 11)
        myStore.addCar(myStore.getLatestCarID(), 'of', 32)
        testCar = myStore.getCarByID(0)
        reIndexedCar = myStore.getCarByID(1)
        myStore.removeCar(0)
        self.assertNotEqual(myStore.storageList[0], testCar)
        self.assertEqual(myStore.storageList[0], reIndexedCar)


    def testgetCarByCarNum(self):
        myStore = CarStorage()
        myStore.addCar(myStore.getLatestCarID(), 'University of Kentucky', 45)
        myStore.addCar(myStore.getLatestCarID(), 'University', 11)
        myStore.addCar(myStore.getLatestCarID(), 'of', 32)
        myCar = myStore.getCarByNum(32)
        self.assertEqual(myStore.storageList[2], myCar)

    def testgetCarByID(self):
        myStore = CarStorage()
        myStore.addCar(myStore.getLatestCarID(), 'University of Kentucky', 45)
        myStore.addCar(myStore.getLatestCarID(), 'University', 11)
        myStore.addCar(myStore.getLatestCarID(), 'of', 32)
        myCar = myStore.getCarByID(1)
        self.assertEqual(myStore.storageList[1], myCar)

    def testgetCarByOrg(self):
        myStore = CarStorage()
        myStore.addCar(myStore.getLatestCarID(), 'University of Kentucky', 45)
        myStore.addCar(myStore.getLatestCarID(), 'University', 11)
        myStore.addCar(myStore.getLatestCarID(), 'of', 32)
        myCar = myStore.getCarByOrg('University')
        self.assertEqual(myStore.storageList[1], myCar)

    def testreindex(self):
        myStore = CarStorage()
        myStore.addCar(myStore.getLatestCarID(), 'University of Kentucky', 45)
        myStore.addCar(myStore.getLatestCarID(), 'University', 12)
        myStore.addCar(myStore.getLatestCarID(), 'of', 33)
        myStore.addCar(myStore.getLatestCarID(), 'Univerity of Kentucky', 42)
        myStore.addCar(myStore.getLatestCarID(), 'Univesity', 1)
        myStore.addCar(myStore.getLatestCarID(), 'of', 2)
        newCar = myStore.getCarByID(1)
        secCar = myStore.getCarByID(2)
        myStore.storageList.remove(newCar)
        myStore.reindexStorage(1)
        self.assertNotEqual(newCar, myStore.storageList[1])
        self.assertEqual(secCar, myStore.storageList[1])

    def appendLapTime(self):
        myStore = CarStorage()
        myStore.addCar(myStore.getLatestCarID(), 'University of Kentucky', 45)
        myCar = myStore.getCarByID(0)
        myStore.appendLapTime(0, 1, 5, 3, 2)
        CarLap = myCar.getLapByID(0)
        self.assertEqual(CarLap[1], 1)
        self.assertEqual(CarLap[2], 5)
        self.assertEqual(CarLap[3], 3)
        self.assertEqual(CarLap[4], 2)


    def testeditLaptime(self):
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

    def testgetCopyStorage(self):
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












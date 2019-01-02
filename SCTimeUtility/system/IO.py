import csv
import os
from SCTimeUtility.table.Car import Car
from SCTimeUtility.table.CarStorage import CarStorage
from SCTimeUtility.log.Log import getLog


def saveCSV(cs, filePath):
    # Save a CarStorage object to a CSV file.
    if filePath != '':
        with open(filePath, "w") as storageFile:
            storageWriter = csv.writer(storageFile)
            storageWriter.writerows(
                [[c.ID, c.TeamName, c.CarNum, c.initialTime] + [t.elapsedTime for t in c.LapList] for c in
                 cs.storageList])


def loadCSV(filePath):
    if filePath != '':
        carList = []
        with open(filePath, "r") as storageFile:
            storageReader = csv.reader(storageFile)
            for row in storageReader:
                carId = int(row[0])
                carOrg = row[1]
                carNum = int(row[2])
                initialTime = float(row[3])
                elapsedTimes = [float(i) for i in row[4:]]
                newCar = Car(carId, carOrg, carNum)
                newCar.initialTime = initialTime
                for time in elapsedTimes:
                    newCar.addLapTime(time)
                carList.append(newCar)
        return carList


def loadTable():
    print("PH")


def saveTable():
    print("PH")


def createDir(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)


def reverseString(self, string):
    return string[::-1]

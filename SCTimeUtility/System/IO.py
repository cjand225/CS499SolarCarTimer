import csv, os

from SCTimeUtility.Table.Car import Car
from SCTimeUtility.Table.CarStorage import CarStorage
from SCTimeUtility.Log.Log import getLog

'''  
    Function: saveCSV
    Parameters: cs, filePath
    Return Value: N/A
    Purpose: Receives an instance of carStorage and a file path in which to dump all the contents of every object
             within CarStorage instance.
'''


def saveCSV(cs, filePath):
    # Save a CarStorage object to a CSV file.
    if filePath != '':
        with open(filePath, "w") as storageFile:
            storageWriter = csv.writer(storageFile)
            storageWriter.writerows(
                [[c.ID, c.TeamName, c.CarNum, c.initialTime] + [t.elapsedTime for t in c.LapList] for c in
                 cs.storageList])


'''  
    Function: loadCSV
    Parameters: filePath
    Return Value: List [car info]
    Purpose: Loads a file assumed to be CSV format, into a list that is returned to the invoker.
'''


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

import csv
from src.table.Car import Car
from src.table.CarStorage import CarStorage

def saveCSV(cs,filePath):
    # Save a CarStorage object to a CSV file.
    with open(filePath,"w") as storageFile:
        storageWriter = csv.writer(storageFile)
        storageWriter.writerows([[c.ID,c.OrgName,c.CarNum,c.initialTime]+[t.elapsedTime for t in c.LapList] for c in cs.storageList])

def loadCSV(filePath):
    carList = []
    with open(filePath,"r") as storageFile:
        storageReader = csv.reader(storageFile)
        for row in storageReader:
            carId = int(row[0])
            carOrg = row[1]
            carNum = int(row[2])
            initialTime = float(row[3])
            elapsedTimes = [float(i) for i in row[4:]]
            newCar = Car(carId,carOrg,carNum)
            newCar.initialTime = initialTime
            for time in elapsedTimes:
                newCar.addLapTime(time)
            carList.append(newCar)
    return carList

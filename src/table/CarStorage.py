"""
    Module: CarStorage
    Purpose: A data structure model created to handle cars and their related functions
             such as IDs, Vehicle Numbers, Organization Names, and Laptimes all conveniently
             stored as more or less a two dimensional list

    Depends On: Car

"""
from PyQt5.QtCore import QObject, pyqtSignal
from src.table.Car import Car
from src.system.TimeReferences import LapTime
from src.system.Validation import carExists
import re
from src.log.Log import getInfoLog, getCriticalLog, getDebugLog, getErrorLog, getWarningLog


class CarStorage(QObject):
    dataModified = pyqtSignal(int, int)

    def __init__(self):
        super().__init__()
        self.storageList = []
        self.LatestCarID = 0
        self.SeedValue = None
        self.timeOffset = None
        self.enableOffset = False

    def setSeedValue(self, seedTime):
        if self.SeedValue is None:
            self.SeedValue = seedTime
            self.setSeeds()

    def setSeeds(self):
        for car in self.storageList:
            car.setSeedValue(self.SeedValue)

    def setTimeOffset(self, offset):
        self.timeOffset = offset

    def enableOffsetTime(self, cond):
        self.enableOffset = cond

    def createCar(self, carNum, carOrg):
        # check valid carNumber and Valid Car Org
        newCar = Car(self.getLatestCarID(), str(carOrg), carNum)
        if self.SeedValue is not None:
            newCar.setSeedValue(self.SeedValue)
        self.storageList.append(newCar)
        self.LatestCarID += 1
        self.dataModified.emit(newCar.ID, 0)
        newCar.lapChanged.connect(lambda l: self.dataModified.emit(newCar.ID, l))

    # runs each size 2 list item through createCar Function
    def createCars(self, list):
        for item in list:
            if(str(item[0]).isdigit()):
                self.createCar(item[0], item[1])
            else:
                self.createCar(item[1], item[0])


    """
         Function: removeCar
         Parameters: self, ID
         Return Value: N/A
         Purpose: Removes a car by its ID number within the list, from the view side, it'll likely
                  be the column number in which the car is placed. After removal, the list is then
                  reindexed to its proper positions starting where the object was removed to the
                  end of the list, to allow for proper ID management.

     """

    def removeCar(self, ID):
        self.storageList.remove(self.getCarByID(ID))
        self.reindexStorage(ID)

    """
         Function: reindexStorage
         Parameters: self, ID
         Return Value: N/A
         Purpose: Reindexes the ID values of each car starting at the ID value given as a parameter,
                  used soley after a removal has been processed to prevent off by 1 errors or out of
                  bounds errors with the StorageList.

     """

    def reindexStorage(self, ID):
        for x in range(ID, len(self.storageList) - 1):
            self.storageList[x].editID(x - 1)
        self.LatestCarID -= 1

    """
         Function: getCarByID
         Parameters: self, ID
         Return Value: Copy of Car at index ID
         Purpose: Used for getting a reference a copy of a specific car within carStorage, typically used
                  for easier access of each car without having to know specifically where its at
                  within carStorage w/ no intentions of altering the original car. Used only when index
                  Number is Known.

     """

    def getCarByID(self, ID):
        if (ID > len(self.storageList)):
            return -1
        else:
            return self.storageList[ID]

    """
         Function: getCarByNum
         Parameters: carNum
         Return Value: copy of Car that contains value CarNum
         Purpose: Used for getting a reference to a copy of a specific car within carStorage, typically used
                  for easier access of each car without having to know specifically where its at
                  within carStorage w/ no intentions of altering the original car. Used when only Vehicle Number
                  is Known.

     """

    def getCarByNum(self, CarNum):
        itemList = [item for item in self.storageList if item.getCarNum() == CarNum]
        item = itemList[0]
        return item

    """
         Function: getCarByOrg
         Parameters: OrgString
         Return Value: copy of Car that contains value orgString
         Purpose:  Used for getting a reference to a copy of a specific car within carStorage, typically used
                  for easier access of each car without having to know specifically where its at
                  within carStorage w/ no intentions of altering the original car. Used when only Vehicle Organization
                  is Known.

     """

    def getCarByOrg(self, OrgString):
        itemList = [item for item in self.storageList if item.getTeam() == OrgString]
        item = itemList[0]
        return item

    """
         Function: appendLapTime
         Parameters: CarID, Hours, Minutes, Seconds, Milliseconds
         Return Value: N/A
         Purpose: Given the CarID, this function will call addLap for the class Car at Index CarID,
                  which will then add the specific lap information to the specified car class given
                  from the parameters.

     """

    def appendLapTime(self, carID, time):
        self.storageList[carID].addLapTime(LapTime(time))
        # self.dataChanged.emit(carId,len

    """
         Function: editLapTime
         Parameters: CarID, LapID, Hours, Minutes, Seconds, Milliseconds
         Return Value: N/A
         Purpose: Given the CarID, this function will call editLap for the class Car at Index CarID,
                  which will then edit the specific lap information to the specified car class given
                  from the parameters.

     """

    def editLapTime(self, carID, LapID, hours, minutes, seconds, milliseconds):
        self.storageList[carID].editLapTime(LapID, hours, minutes, seconds, milliseconds)

    """
         Function: removeLapTime
         Parameters: CarID, LapID
         Return Value: N/A
         Purpose: Given the CarID, this function will call removeLapTime for the class Car at Index CarID,
                  which will then add the specific lap information to the specified car class given
                  from the parameters.

     """

    def removeLapTime(self, carID, LapID):
        self.getCarByID(carID).removeLapTime(LapID)

    """
         Function: getCarListCopy
         Parameters: self
         Return Value: copy of StorageList
         Purpose: Used for getting a copy of the model for usage within other modules within the Application
                  such as view comonents like graphing/TableView/etc.

     """

    def getCarListCopy(self):
        return self.storageList.copy()


    """
         Function: getCarNamesList
         Parameters: self
         Return Value: list of Org names of all cars
         Purpose: used as a convient method for accesing all the car Orgs Names

     """

    def getCarNamesList(self):
        newList = self.storageList.copy()
        names = []
        for x in range(0, len(newList)):
            names.append(newList[x].getTeam())
        return names

    """
         Function: getLatestCarID
         Parameters: self
         Return Value: LatestCarID(int)
         Purpose: Used for finding what the next ID to be used for the carStorage list should be.

     """

    def getLatestCarID(self):
        return self.LatestCarID

    """
        
        Function: getCarAmount
        Parameters: self
        Return Value: N/A
        Purpose: Used to find how many cars are stored within CarStorage
    
    """

    def getCarAmount(self):
        return len(self.storageList)

    """

        Function: getHighestLapCount
        Parameters: self
        Return Value: N/A
        Purpose: Used to find the highest amount of laps stored within all the cars in carStorage

    """

    def getHighestLapCount(self):
        newList = self.storageList.copy()
        highest = 0
        names = []
        for x in range(0, len(newList)):
            if newList[x].getLapCount() > highest:
                highest = newList[x].getLapCount()
        return highest


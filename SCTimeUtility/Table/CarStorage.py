"""
    Module: CarStorage
    Purpose: A data structure model created to handle cars and their related functions
             such as IDs, Vehicle Numbers, Organization Names, and Laptimes all conveniently
             stored as more or less a two dimensional list

    Depends On: Car

"""

import copy

from PyQt5.QtCore import QObject, pyqtSignal

from SCTimeUtility.Table.Car import Car
from SCTimeUtility.Table.LapTime import LapTime
from SCTimeUtility.Log.Log import getLog


class CarStorage(QObject):
    dataModified = pyqtSignal(int, int)

    def __init__(self):
        super().__init__()
        self.logger = getLog()
        self.storageList = []
        self.SeedValue = None
        self.timeOffset = None
        self.enableOffset = False

    """
          Function: setSeedValue
          Parameters: self, seedTime
          Return Value: N/A
          Purpose: Function that sets the Seed Value of Car Storage and then calls setSeeds to globally
                  set that value for each car.

    """

    def setSeedValue(self, seedTime):
        if self.SeedValue is None and len(self.storageList) > 0:
            self.SeedValue = seedTime
            self.logger.info('[' + __name__ + ']' + 'Setting Seed Value for All Cars')
            self.setSeeds()

    """
          Function: setSeeds
          Parameters: self
          Return Value: N/A
          Purpose: Function that sets the Seed Value of each car with the value of the "Global" SeedValue
                   that is stored within Car Storage.

    """

    def setSeeds(self):
        for car in self.storageList:
            car.setSeedValue(self.SeedValue)

    """
          Function: setOffsetTime
          Parameters: self, cond
          Return Value: N/A
          Purpose: Function that offsets absolute times calculated for reporting the time of day.

    """

    def setTimeOffset(self, offset):
        self.timeOffset = offset

    """
          Function: enableOffsetTime
          Parameters: self, cond
          Return Value: N/A
          Purpose: Function that flags CarStorage to offset the time of all the cars to better fit
                   the Time supplied to it. (May be deprecated later.)

    """

    def enableOffsetTime(self, cond):
        self.enableOffset = cond

    """
          Function: createCars
          Parameters: self, list
          Return Value: N/A
          Purpose: Goes through list parameter, checks if the first item is a digit. If so, it assumes
                   that is it the car number and creates that car with Item 0 as ID and Item 1 as Team Name,
                   otherwise it assumes Item 1 is ID and Item 0 is Team Name. Validation is done via
                   AddBatchDialog.

    """

    def createCar(self, carNum, teamName):
        # check valid carNumber and Valid Car Org
        newCar = Car(self.getLatestCarID(), str(teamName), carNum)
        if self.SeedValue is not None:
            newCar.setSeedValue(self.SeedValue)
        self.storageList.append(newCar)
        self.dataModified.emit(newCar.ID, 0)
        newCar.lapChanged.connect(lambda l: self.dataModified.emit(newCar.ID, l))
        self.logger.info('[' + __name__ + ']' + 'Adding Car: {} , {}'.format(teamName, carNum))

    """
          Function: createCars
          Parameters: self, list
          Return Value: N/A
          Purpose: Goes through list parameter, checks if the first item is a digit. If so, it assumes
                   that is it the car number and creates that car with Item 0 as ID and Item 1 as Team Name,
                   otherwise it assumes Item 1 is ID and Item 0 is Team Name. Validation is done via
                   AddBatchDialog.

    """

    def createCars(self, list):
        index = 0
        for item in list:
            # print(len(list))
            if len(item) == 2:
                self.createCar(item[1], item[0])
            else:
                continue
            index += 1

    """
         Function: removeCar
         Parameters: self, ID
         Return Value: N/A
         Purpose: Removes a car by its ID number within the list, from the view side, it'll likely
                  be the column number in which the car is placed. After removal, the list is then
                  re-indexed to its proper positions starting where the object was removed to the
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
            self.storageList[x].setID(x - 1)

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
        if ID in range(0, len(self.storageList) - 1):
            return self.storageList[ID]
        else:
            return False

    """
         Function: getCarByNum
         Parameters: carNum
         Return Value: copy of Car that contains value CarNum
         Purpose: Used for getting a reference to a copy of a specific car within carStorage, typically used
                  for easier access of each car without having to know specifically where its at
                  within carStorage w/ no intentions of altering the original car. Used when only Vehicle Number
                  is Known.

    """

    def getCarByNum(self, carNum):
        for item in self.storageList:
            if item.getCarNum() == carNum:
                return item

    """
         Function: getCarByTeamName
         Parameters: OrgString
         Return Value: copy of Car that contains value teamName
         Purpose:  Used for getting a reference to a copy of a specific car within carStorage, typically used
                  for easier access of each car without having to know specifically where its at
                  within carStorage w/ no intentions of altering the original car. Used when only Vehicle Organization
                  is Known.

    """

    def getCarByTeamName(self, teamName):
        itemList = [item for item in self.storageList if item.getTeam() == teamName]
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
        self.storageList[carID].addLapTime(time)
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
                  such as view components like graphing/TableView/etc.

    """

    def getCarListCopy(self):
        storageCopy = []
        storageCopy.clear()
        for car in range(0, len(storageCopy) - 1):
            storageCopy.append(copy.deepcopy(self.storageList[car]))
        return storageCopy  # .copy()

    """
         Function: getCarNames
         Parameters: self
         Return Value: list of Org names of all cars
         Purpose: Used as a convenient method for accessing all the cars' Team Name.

    """

    def getCarNames(self):
        newList = self.storageList.copy()
        names = []
        for x in range(0, len(newList)):
            names.append(newList[x].getTeam())
        return names

    """
         Function: getLatestCarID
         Parameters: self
         Return Value: LatestCarID(int)
         Purpose: gives the next ID to be used, which is the length of the storageList

    """

    def getLatestCarID(self):
        return len(self.storageList)

    """
        
        Function: getCarCount
        Parameters: self
        Return Value: N/A
        Purpose: Used to find how many cars are stored within CarStorage
    
    """

    def getCarCount(self):
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

    def startCar(self, index):
        pass

    def stopCar(self, index):
        pass

    def startAllCars(self):
        pass

    def stopAllCars(self):
        pass

import time

from PyQt5.QtCore import pyqtSignal, QObject

from SCTimeUtility.Table.LapTime import LapTime
from SCTimeUtility.System.Validation import intToTimeStr
from SCTimeUtility.Log.Log import getLog


class Car(QObject):
    lapChanged = pyqtSignal(int)

    def __init__(self, ID, Team, CarNum):
        super().__init__()
        self.logger = getLog()

        try:
            self.ID = int(ID)
            self.CarNum = int(CarNum)
        except ValueError:
            raise ValueError

        if type(Team) is not str:
            raise ValueError
        else:
            self.TeamName = str(Team)

        if not self.ID:
            self.ID = -1
        if not self.CarNum:
            self.CarNum = -1

        self.SeedValue = None
        self.initialTime = None

        self.LapCount = 0
        self.LapList = []

    """
          Function: setSeedValue
          Parameters: self, value
          Return Value: N/A
          Purpose: sets the member variable "self.SeedValue" to the value parameter passed, and then
                   calls createFirstLap before returning. Used for initializing lap times for each car.

    """

    def setSeedValue(self, value):
        self.SeedValue = value
        self.createFirstLap()

    """
          Function: getSeedValue
          Parameters: self
          Return Value: self.SeedValue
          Purpose: returns the seed value at which all lap times are based upon, otherwise known as 
                   starting time.

    """

    def getSeedValue(self):
        return self.SeedValue

    """
          Function: createFirstLap
          Parameters: self
          Return Value: N/A
          Purpose: creates the first lap of the car based on seed value, emits that the 
                    object has been changed for model to update to view.

    """

    def createFirstLap(self):
        self.LapList.clear()
        self.LapList.append(LapTime(self.SeedValue - self.SeedValue))
        self.LapCount = len(self.LapList)
        self.lapChanged.emit(len(self.LapList))

    """
          Function: getID
          Parameters: self
          Return Value: self.ID
          Purpose: returns the currently set carID, primarily used with indexing lists
  
    """

    def getID(self):
        return self.ID

    """
         Function: getTeam
         Parameters: self
         Return Value: self.TeamName
         Purpose: Returns the currently set Team name, used as part of a search and ease of access
  
    """

    def getTeam(self):
        return self.TeamName

    """
         Function: getCarNum
         Parameters: self
         Return Value: self.CarNum
         Purpose: Returns the currently set CarNum, used as part of a search function and ease of access.
  
    """

    def getCarNum(self):
        return self.CarNum

    """
         Function: setID
         Parameters: self, ID
         Return Value: N/A
         Purpose: Edits the currently set self.ID to a new ID, used as part of a indexing function within
                  CarStorage class.
  
    """

    def setID(self, ID):
        self.ID = ID

    """
  
        Function: getLapCount
        Parameters: self
        Return Value: self.LapCount
        Purpose: Returns the total laps that have been added to the car class.
  
    """

    def getLapCount(self):
        return len(self.LapList)

    """
        Function: addLapTime
        Parameters: self, timeData
        Return Value: N/A
        Purpose: Function that gets called when needing to add a laptime to a car, checks if the car
                 has a set seedvalue (if it doesn't, nothing gets recorded), then proceeds to check if
                 a parameter has been supplied or not, which if it has will understand that the lap was
                 inputted manually, if not, it understands that the lap was inputted via Semi-Auto widget,
                 after which it then emits the new lapList length to be updated in the model.
  
    """

    def addLapTime(self, timeData=None):
        if self.SeedValue is not None:
            if timeData is None:
                self.addLapSemiAuto()
            else:
                self.addLapManually(timeData)
            self.LapCount = len(self.LapList)
            self.lapChanged.emit(len(self.LapList))

    """
        Function: addLapSemiAuto
        Parameters: self
        Return Value: N/A
        Purpose: appends a laptime to the current LapList of the Car based on the amount of time
                 that has passed and all previous laptimes, invoke via user interface by user within
                 the Semi-Auto widget.

    """

    def addLapSemiAuto(self):
        timeBeforeIndex = self.getTotalElapsedTime(self.getLapCount())
        timeSinceStart = time.time() - self.SeedValue
        recordedTime = 0

        if timeBeforeIndex == -1:
            recordedTime = timeSinceStart
        else:
            recordedTime = timeSinceStart - timeBeforeIndex

        # time couldn't have possibly occured as race hasn't lastest long enough
        if recordedTime < 0:
            recordedTime = 0

        self.LapList.append(LapTime(int(recordedTime)))
        self.logger.info(
            'Lap Time {} added Car: {} , {} via SemiAuto.'.format(intToTimeStr(int(recordedTime)),
                                                                  self.TeamName,
                                                                  self.CarNum))

    """
        Function: addLapManually
        Parameters: self
        Return Value: N/A
        Purpose: invoked via addLapTime, understands that a parameter called time data has been applied and then adds
                 that time to the end of the lap list.

    """

    def addLapManually(self, timeData):
        self.LapList.append(LapTime(timeData))
        self.logger.info(
            'Lap Time {} added Car: {} , {} via Manual.'.format(intToTimeStr(int(timeData)), self.TeamName,
                                                                self.CarNum))

    """
         Function: editLapTime
         Parameters: self, index, timeData
         Return Value: N/A
         Purpose: Edits current given index in lapList, if lap below given index exists, the lap below is
                  offset by the difference between the lap below's value and the newly given value from
                  timeData.
  
     """

    def editLapTime(self, index, timeData):
        editCondition = False
        edit = timeData
        # both cell above and cell below exists
        if self.indexExists(index) and self.indexExists(index + 1) and timeData is not None and timeData >= 0:

            totalTime = self.LapList[index].elapsedTime + self.LapList[index + 1].elapsedTime
            editBelow = totalTime - edit

            # edit both cells with new edit
            if self.editCell(index, edit) and self.editCell(index + 1, editBelow):
                editCondition = True
                self.logger.info('Lap {} edited for Car: {} , {} '.format(index, self.TeamName, self.CarNum))
            else:
                self.logger.info('Failed to Edit Lap {} for Car: {} '.format(index, self.ID))
        # if the index given is the last index in the list
        elif self.indexExists(index) and not self.indexExists(index + 1) and timeData is not None and timeData >= 0:
            # only current index cell exists
            if self.editCell(index, edit):
                editCondition = True
                self.logger.info('Lap {} edited for Car: {} , {} '.format(index, self.TeamName, self.CarNum))
            else:
                self.logger.info('Failed to Edit Lap {} for Car: {} '.format(index, self.ID))
        else:
            self.logger.info(
                "Failed to Edit Lap {} for Car: {} : Index isn't within range of LapList".format(index, self.ID))

        self.lapChanged.emit(len(self.LapList))
        return editCondition

    """
         Function: editCell
         Parameters: self index, timeData
         Return Value: Boolean Condition
         Purpose: Returns a Boolean Condition to indicate whether a cell(LapTime) has been edited

     """

    def editCell(self, index, timeData):
        if self.indexExists(index):
            self.LapList[index].elapsedTime = timeData
            return True
        else:
            return False

    """
         Function: indexExists
         Parameters: self, index
         Return Value: Boolean Condition
         Purpose: Returns a Boolean Condition to indicate whether an index is within range of the LapList

     """

    def indexExists(self, index):
        return index in range(0, len(self.LapList))

    """
         Function: getLap
         Parameters: self ID
         Return Value: copy of Lap, found by an Index ID
         Purpose: Returns the Lap found at the index ID.
    
     """

    def getLap(self, lapID):
        if lapID in range(0, len(self.LapList)):
            return self.LapList[lapID]
        else:
            return LapTime(-1)

    """
         Function: getLastLapIndex
         Parameters: self
         Return Value: int
         Purpose: Returns the index postion of the last element in the laplist

     """

    def getLastLapIndex(self):
        return len(self.LapList) - 2

    """
         Function: removeLapTime
         Parameters: self, lapID
         Return Value: N/A
         Purpose: Zeros out the laptime given by lapID. Mainly implemented with the assumption that
                  the user does not want the amount of laps to change but may simply want to delete
                  a specified lap in order to put in more accurate data later.
    
     """

    def removeLapTime(self, lapID):
        if lapID in range(1, len(self.LapList) - 1):
            self.LapList[lapID].clear()
            self.logger.info('Lap {} removed for Car: {} , {}!'.format(lapID, self.TeamName, self.CarNum))
            return True
        else:
            self.logger.info('Failed to Remove Lap {} for Car: {} , {}!'.format(lapID, self.TeamName, self.CarNum))
            self.logger.debug('Lap Removal {}, Car: {}: Invalid Index'.format(lapID, self.ID))
            return False

    """
         Function: getLatestLapID
         Parameters: self
         Return Value: LatestLapID(Int)
         Purpose: Returns an integer that would be the current ID to be used for next lap input.
    
     """

    def getLatestLapID(self):
        return len(self.LapList) - 1

    """
         Function: getTotalElaspedTime
         Parameters: self, index
         Return Value: totalElasped (elapsed Time)
         Purpose: Sums the total elapsed time since the seedValue as occured and returns it as time var
    
     """

    def getTotalElapsedTime(self, index):
        if not index in range(0, len(self.LapList) - 1):
            allLaps = self.LapList[1:index]
            return sum([lap.getElapsed() for lap in allLaps])
        else:
            return -1

    """
         Function: getFasestLap
         Parameters: self, index
         Return Value: fastestLap (in seconds)
         Purpose: gets the fastest lap that has happened within lapList, Initially is None, and adds the first
                  lap that is greater than 0 if the current fastLap is none, then when it has a value, if the value
                  in the list is lower, it chooses that value for the new fastLap value and repeats until the lowest
                  value has been found.
    
     """

    def getFastestLap(self):
        allLaps = self.LapList[1:]
        if allLaps:
            return min([lap.getElapsed() for lap in allLaps])
        else:
            return None

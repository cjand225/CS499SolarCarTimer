"""

    Module:
    Purpose:
    Depends On:

"""

import datetime

from PyQt5.QtCore import pyqtSignal, QObject

from SCTimeUtility.Table.LapTime import LapTime
from SCTimeUtility.Log.Log import get_log


class Car(QObject):
    lapChanged = pyqtSignal(int)
    runningSignal = pyqtSignal(int, bool)

    def __init__(self, ID, Team, CarNum):
        super().__init__()
        self.logger = get_log()

        try:
            self.ID = int(ID)
            self.CarNum = int(CarNum)
            self.TeamName = str(Team)
        except ValueError as err:
            self.logger.error(err)

        self.seedValue = None
        self.running = False

        self.lapCount = 0
        self.lapList = []

    """
          Function: setSeedValue
          Parameters: self, value
          Return Value: N/A
          Purpose: sets the member variable "self.seedValue" to the value parameter passed, and then
                   calls createFirstLap before returning. Used for initializing lap times for each car.

    """

    def setSeedValue(self, value):
        if isinstance(value, datetime.datetime):
            self.seedValue = value
            self.createFirstLap()
            self.running = True
            self.runningSignal.emit(self.ID, self.running)
        else:
            raise TypeError("Seed Value is incorrect type" + str(type(value)))

    """
          Function: getSeedValue
          Parameters: self
          Return Value: self.seedValue
          Purpose: returns the seed value at which all lap times are based upon, otherwise known as 
                   starting time.

    """

    def getSeedValue(self):
        return self.seedValue

    """
          Function: createFirstLap
          Parameters: self
          Return Value: N/A
          Purpose: creates the first lap of the car based on seed value, emits that the 
                    object has been changed for model to update to view.

    """

    def createFirstLap(self):
        self.lapList.clear()
        self.lapList.append(LapTime(datetime.timedelta(0)))
        self.lapCount = len(self.lapList)
        self.lapChanged.emit(len(self.lapList))

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
        Return Value: self.lapCount
        Purpose: Returns the total laps that have been added to the car class.
  
    """

    def getLapCount(self):
        return len(self.lapList)

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
        if self.seedValue is not None:
            if timeData is None:
                self.addLapSemiAuto()
            else:
                self.addLapManually(timeData)
            self.lapCount = len(self.lapList)
            self.lapChanged.emit(len(self.lapList))

    """
        Function: addLapSemiAuto
        Parameters: self
        Return Value: N/A
        Purpose: appends a LapTime to the current lapList of the Car based on the amount of time
                 that has passed and all previous laptimes, invoke via user interface by user within
                 the Semi-Auto widget.

    """

    def addLapSemiAuto(self):
        currentTime = datetime.datetime.now()
        beginTime = self.seedValue
        previousTime = self.lapList[self.lapCount - 1].initial_write
        recordTime = datetime.timedelta(hours=currentTime.hour,
                                        minutes=currentTime.minute,
                                        seconds=currentTime.second,
                                        microseconds=currentTime.microsecond) \
                     - \
                     datetime.timedelta(hours=previousTime.hour,
                                        minutes=previousTime.minute,
                                        seconds=previousTime.second,
                                        microseconds=previousTime.microsecond)

        totalTime = datetime.timedelta(hours=currentTime.hour,
                                       minutes=currentTime.minute,
                                       seconds=currentTime.second,
                                       microseconds=currentTime.microsecond) \
                    - \
                    datetime.timedelta(hours=beginTime.hour,
                                       minutes=beginTime.minute,
                                       seconds=beginTime.second,
                                       microseconds=beginTime.microsecond)

        if not recordTime > totalTime:
            self.lapList.append(LapTime(recordTime))
            self.logger.info('Lap Time {} added Car: {} , {} via SemiAuto.'.format(recordTime,
                                                                                   self.TeamName,
                                                                                   self.CarNum))
        else:
            self.logger.info('Unable to add Lap Time {} for Car: {} , {} via SemiAuto.'.format(recordTime,
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
        self.lapList.append(LapTime(timeData))
        self.logger.info(
            'Lap Time {} added Car: {} , {} via Manual.'.format(timeData,
                                                                self.TeamName,
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
        if self.indexExists(index) and self.indexExists(
                index + 1) and timeData is not None and timeData.total_seconds() >= 0:

            totalTime = self.lapList[index].elapsedTime + self.lapList[index + 1].elapsedTime
            editBelow = totalTime - edit

            # edit both cells with new edit
            if self.editCell(index, edit) and self.editCell(index + 1, editBelow):
                editCondition = True
                self.logger.info('Lap {} edited for Car: {} , {} '.format(index, self.TeamName, self.CarNum))
            else:
                self.logger.info('Failed to Edit Lap {} for Car: {} '.format(index, self.ID))
        # if the index given is the last index in the list
        elif self.indexExists(index) and not self.indexExists(
                index + 1) and timeData is not None and timeData.total_seconds() >= 0:
            # only current index cell exists
            if self.editCell(index, edit):
                editCondition = True
                self.logger.info('Lap {} edited for Car: {} , {} '.format(index, self.TeamName, self.CarNum))
            else:
                self.logger.info('Failed to Edit Lap {} for Car: {} '.format(index, self.ID))
        else:
            self.logger.info(
                "Failed to Edit Lap {} for Car: {} : Index isn't within range of lapList".format(index, self.ID))

        self.lapChanged.emit(len(self.lapList))
        return editCondition

    """
         Function: editCell
         Parameters: self index, timeData
         Return Value: Boolean Condition
         Purpose: Returns a Boolean Condition to indicate whether a cell(LapTime) has been edited

     """

    def editCell(self, index, timeData):
        if self.indexExists(index):
            self.lapList[index].set_elapsed(timeData)
            return True
        else:
            return False

    """
         Function: indexExists
         Parameters: self, index
         Return Value: Boolean Condition
         Purpose: Returns a Boolean Condition to indicate whether an index is within range of the lapList

     """

    def indexExists(self, index):
        return index in range(0, len(self.lapList))

    """
         Function: getLap
         Parameters: self ID
         Return Value: copy of Lap, found by an Index ID
         Purpose: Returns the Lap found at the index ID.
    
     """

    def getLap(self, lapID):
        if lapID in range(0, len(self.lapList)):
            return self.lapList[lapID]
        else:
            raise IndexError("LapID: " + str(lapID) + " out of range.")

    """
         Function: getLastLapIndex
         Parameters: self
         Return Value: int
         Purpose: Returns the index postion of the last element in the laplist

     """

    def getLastLapIndex(self):
        return len(self.lapList) - 2

    """
         Function: removeLapTime
         Parameters: self, lapID
         Return Value: N/A
         Purpose: Zeros out the laptime given by lapID. Mainly implemented with the assumption that
                  the user does not want the amount of laps to change but may simply want to delete
                  a specified lap in order to put in more accurate data later.
    
     """

    def removeLapTime(self, lapID):
        if lapID in range(1, len(self.lapList) - 1):
            self.lapList[lapID].clear()
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
        return len(self.lapList) - 1

    """
         Function: getTotalElaspedTime
         Parameters: self, index
         Return Value: totalElasped (elapsed Time)
         Purpose: Sums the total elapsed time since the seedValue as occured and returns it as time var
    
     """

    def getTotalElapsedTime(self, index):
        if not index in range(0, len(self.lapList) - 1):
            allLaps = self.lapList[1:index]
            return sum([lap.get_elapsed_time() for lap in allLaps])
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
        allLaps = self.lapList[1:]
        if allLaps:
            return min([lap.get_elapsed_time() for lap in allLaps])
        else:
            return None

    #TODO
    def hasSeed(self):
        if isinstance(self.seedValue, datetime.datetime):
            return True
        else:
            return False
    #TODO
    def editTeamName(self, newName):
        if isinstance(newName, str):
            self.TeamName = newName
    #TODO
    def editCarNumber(self, newNumber):
        if isinstance(newNumber, int):
            self.CarNum = newNumber
    #TODO
    def stop(self):
        if self.running:
            self.running = False
            self.runningSignal.emit(self.ID, self.running)
    #TODO
    def start(self):
        # Initial State of Car before starting first time
        if not self.running and not self.seedValue:
            self.running = True
            self.setSeedValue(datetime.datetime.now())
            self.runningSignal.emit(self.ID, self.running)
        # Pause State from Car, Resume, added a new seedValue
        elif not self.running and isinstance(self.seedValue, datetime.datetime):
            self.running = True
            self.runningSignal.emit(self.ID, self.running)
    #TODO
    def isRunning(self):
        return self.running

import time
from PyQt5.QtCore import pyqtSignal, QObject
from src.system.TimeReferences import LapTime
from src.system.Validation import intergerToTimeString
from datetime import timedelta
from src.log.Log import getInfoLog, getCriticalLog, getDebugLog, getErrorLog, getWarningLog


class Car(QObject):
    lapChanged = pyqtSignal(int)

    def __init__(self, ID, Team, CarNum):
        super().__init__()
        self.ID = ID
        self.TeamName = str(Team)
        self.CarNum = CarNum

        self.SeedValue = None
        self.initialTime = None

        self.LapCount = 0
        self.LapList = []

    # Car Related
    def setSeedValue(self, value):
        self.SeedValue = value
        self.createFirstLap()

    def getSeedValue(self):
        return self.SeedValue

    def createFirstLap(self):
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
        return self.LapCount

    """
        Function: addLapTime
        Parameters: self, hours, minutes, seconds, milliseconds
        Return Value: N/A
        Purpose: appends a laptime to the current LapList of the Car, and then increments what the
                 next ID to be used for the next Lap that will be.
  
    """

    def addLapTime(self, timeData=None):
        if self.SeedValue is not None:
            if timeData is None:
                self.addLapSemiAuto()
            elif timeData.getElapsed() is not None:
                self.addLapManually(timeData)

            self.LapCount = len(self.LapList)
            self.lapChanged.emit(len(self.LapList))

    def addLapSemiAuto(self):
        timeBeforeIndex = self.getTotalElapsedTime(self.LapCount)
        timeSinceStart = time.time() - self.SeedValue
        recordedTime = 0

        if (round(timeBeforeIndex) <= 0):
            recordedTime = timeSinceStart
        else:
            recordedTime = timeSinceStart - timeBeforeIndex

        # time couldn't have possibly occured as race hasn't lastest long enough
        if (recordedTime < 0):
            recordedTime = 0

        getInfoLog().info('Lap Added to Car: {}')
        self.LapList.append(LapTime(int(recordedTime)))
        getInfoLog().info('Lap Time {} added Car: {} , {} by SemiAuto.'.format(intergerToTimeString(int(recordedTime)),self.TeamName, self.CarNum))

    def addLapManually(self, timeData):
        self.LapList.append(LapTime(timeData))
        getInfoLog().info('Lap Time {} added Car: {} , {} by Manual.'.format(intergerToTimeString(int(timeData)),self.TeamName, self.CarNum))

    """
         Function: editLapTime
         Parameters: self, index, timeData(inputted as SS -> MM -> HH) like on a stopwatch
         Return Value: N/A
         Purpose: Edits the current index with new time and offsets the index+1 laptime to keep time
                  consistent, if the time is greater than the total time of the cells, we assume
                  user would like to 0 out the index + 1 cell, afterwards, emits a signal to tell the Model
                  to update.
  
     """

    def editLapTime(self, index, timeData):
        if index != 0 and index < len(self.LapList):
            oldTime = self.LapList[index].getElapsed()
            newTime = timeData
            timeDiff = oldTime - newTime

            self.LapList[index].setElapsed(newTime)

            # valid index + 1, so another cell exists below current cell
            if index < len(self.LapList) - 1:
                cellBelow = self.LapList[index + 1].getElapsed()
                totalTime = oldTime + cellBelow

                if newTime <= totalTime:
                    self.LapList[index + 1].setElapsed(cellBelow + timeDiff)
                else:
                    self.LapList[index + 1].setElapsed(0)

            self.lapChanged.emit(len(self.LapList))
            getInfoLog().info('Lap {} edited for Car: {} , {} '.format(index, self.TeamName, self.CarNum))

    """
         Function: getLap
         Parameters: self ID
         Return Value: copy of Lap, found by an Index ID
         Purpose: Returns the Lap found at the index ID.
  
     """

    def getLap(self, lapID):
        return self.LapList[lapID]

    """
         Function: removeLapTime
         Parameters: self, lapID
         Return Value: N/A
         Purpose: "Removes" a Laptime in the sense that it will Zero out whatever laptime given at the
                  current index denoted by lapID. Mainly implemented this way with the assumption that
                  the user does not want the amount of laps to change but may simply want to delete
                  a specified lap in order to put in more accurate data later.
  
     """

    def removeLapTime(self, lapID):
        self.LapList[lapID] = LapTime(self.SeedValue - self.SeedValue)
        getInfoLog().info('Lap {} removed for Car: {} , {} '.format(lapID, self.TeamName, self.CarNum))

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
        totalElasped = 0
        for currLap in range(0, index):
            totalElasped += int(self.LapList[currLap].getElapsed())
        return totalElasped

    """
         Function: getFasestLap
         Parameters: self, index
         Return Value: fastestLap (in seconds)
         Purpose: gets the fastest lap that has happened within lapList, Initalially is None, and adds the first
                  lap that is greater than 0 if the current fastLap is none, then when it has a value, if the value
                  in the list is lower, it chooses that value for the new fastLap value and repeats until the lowest
                  value has been found.

     """
    def getFastestLap(self):
        allLaps = self.LapList[1:]
        if allLaps:
            # for lap in self.LapList:
            #     if lap.getElapsed() > 0 and fastLap == 999:
            #         fastLap = lap.getElapsed()
            #     else:
            #         if fastLap is not None:
            #             if fastLap > lap.getElapsed() and lap.getElapsed() > 0:
            #                 fastLap = lap.getElapsed()
            # print([lap.getElapsed() for lap in allLaps])
            return min([lap.getElapsed() for lap in allLaps])
        else:
            return None
                            

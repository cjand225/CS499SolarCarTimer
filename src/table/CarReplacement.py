from time import time
from PyQt5.QtCore import pyqtSignal, QObject
from src.system.Time import LapTime
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

  def createFirstLap(self):
    self.LapList.append(LapTime(self.SeedValue - self.SeedValue))

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
    totalElapsed = self.getTotalElaspedTime(self.LapCount - 1)
    if timeData is None:
      ElaspedTime = totalElapsed + self.SeedValue
      self.LapList.append(ElaspedTime)
      self.lapChanged.emit(len(self.LapList))
    else:
      if timeData < totalElapsed + 30:
        self.LapList.append(timeData)
        self.lapChanged.emit(len(self.LapList))
    self.LapCount += 1

  """
       Function: editLapTime
       Parameters: self, ID, Hours, minutes, seconds, milliseconds
       Return Value: N/A
       Purpose: edits the laptime at the index ID, by reassigning its ID, and lap data to
                that specific item with the lapList. Used with the assumption a user wants
                to delete a lap and then re-enter other data.

   """

  def editLapTime(self, index, timeData):
    if index == 0 or index > len(self.LapList):
      return
    else:
      totalElapsed = self.getTotalElaspedTime(self.LapCount - 1)
      if timeData < totalElapsed + 30:
        self.LapList[index].setElapsed(timeData)
        self.lapChanged.emit(len(self.LapList))

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

  """
       Function: getLatestLapID
       Parameters: self
       Return Value: LatestLapID(Int)
       Purpose: Returns an integer that would be the current ID to be used for next lap input.

   """

  def getLatestLapID(self):
    return len(self.LapList) - 1

  """
       Function: getTotalElaspedTimeUpToIndex
       Parameters: self, index
       Return Value: totalElasped (elapsed Time)
       Purpose: Sums the total elapsed time since the seedValue as occured and returns it as time var

   """
  def getTotalElaspedUpToIndex(self, index):
    totalElasped = 0
    if index == 0 or index > len(self.LapList):
      totalElasped = 0
    else:
      for currLap in range(0, index - 1):
        totalElasped += self.LapList[currLap].ElapsedTime()
    return totalElasped

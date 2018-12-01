"""
    Module: Car
    Purpose: a struct like class, designed to hold information within the model
             about a specific Object in the real world, in this case it holds
             a vehicle number, Organization Name, and Lap times associated with
             the the vehicle.

    Depends On: N/A

"""

from time import time
from PyQt5.QtCore import pyqtSignal, QObject
from src.system.Time import Lap_Time
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

    self.LatestLapID = 0
    self.LapCount = 0
    self.LapList = []

  """
      Function: addLapTime
      Parameters: self, hours, minutes, seconds, milliseconds
      Return Value: N/A
      Purpose: appends a laptime to the current LapList of the Car, and then increments what the
               next ID to be used for the next Lap that will be.
  
  """

  # def addLapTime(self, hours, minutes, seconds, milliseconds):
  #     newLap = [self.getLatestLapID(), hours, minutes, seconds, milliseconds]
  #     self.LapList.insert(self.LatestLapID, newLap)
  #     self.LatestLapID += 1
  #     self.LapCount = len(self.LapList)
  #     self.lapChanged.emit(len(self.LapList))

  # TODO: Make time optional, if no time given, take elasped time count (for semi auto)
  def addLapTime(self, time=None):
    recordedTime = None

    # assumes that semi-auto is calling it
    if time == None:
      time = 23
      self.LapList.append(Lap_Time(recordedTime, time))
      self.lapChanged.emit(len(self.LapList))
    else:
      if self.LapList:
        recordedTime = self.LapList[-1].recordedTime + time
      else:
        recordedTime = self.initialTime
      self.LapList.append(Lap_Time(recordedTime, time))
      self.lapChanged.emit(len(self.LapList))

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
    self.LapList[lapID] = [lapID, 0, 0, 0, 0]

  """
       Function: editLapTime
       Parameters: self, ID, Hours, minutes, seconds, milliseconds
       Return Value: N/A
       Purpose: edits the laptime at the index ID, by reassigning its ID, and lap data to
                that specific item with the lapList. Used with the assumption a user wants
                to delete a lap and then re-enter other data.

   """

  # def editLapTime(self, ID, hours, minutes, seconds, milliseconds=None):
  #     if(milliseconds):
  #         self.LapList[ID] = [ID, hours, minutes, seconds, milliseconds]
  #     else:
  #         self.LapList[ID] = [ID, hours, minutes, seconds, 0]
  #     self.lapChanged.emit(ID)

  def editLapTime(self, ID, time):
    self.LapList[ID].elapsedTime = time
    if ID == 0:
      self.LapList[ID].recordedTime = self.initialTime + time
    else:
      self.LapList[ID].recordedTime = self.LapList[ID - 1].recordedTime + time
    for lapIndex in range(ID + 1, len(self.LapList)):
      self.LapList[lapIndex].recordedTime = self.LapList[lapIndex - 1].recordedTime + self.LapList[
        lapIndex].elapsedTime

  """
       Function: getLatestLapID
       Parameters: self
       Return Value: LatestLapID(Int)
       Purpose: Returns an integer that would be the current ID suggested to be used
                when adding Laps to the LapList.

   """

  def getLatestLapID(self):
    return len(self.LapList)


  """
       Function: getLapByID
       Parameters: self ID
       Return Value: copy of Lap, found by an Index ID
       Purpose: Returns a copy of the Lap found at the index ID, such that a user can have
                access to a lap without worry of modifying its' contents.

   """

  def getLapByID(self, ID):
    newlist = self.LapList.copy()
    if (ID >= self.LapCount):
      return None
    else:
      return newlist[ID]

  """
       Function: getCarID
       Parameters: self
       Return Value: self.ID
       Purpose: returns the currently set carID, primarily used with indexing lists

   """

  def getCarID(self):
    return self.ID

  """
       Function: getTeam
       Parameters: self
       Return Value: self.TeamName
       Purpose: Returns the currently set TeamName, used as part of a search and ease of access

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
       Function: editID
       Parameters: self, ID
       Return Value: N/A
       Purpose: Edits the currently set self.ID to a new ID, used as part of a indexing function within
                CarStorage class.

   """

  def editID(self, ID):
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
  
  """

  def getLap(self, lapID):
    return self.LapList[lapID]


  def getTotalElaspedUpToIndex(self, index):
    totalElasped = 0
    if index == 0 or index > len(self.LapList):
      totalElasped = 0
    else:
      for currLap in range(0, index - 1):
        totalElasped += self.LapList[currLap].ElapsedTime()
    return totalElasped

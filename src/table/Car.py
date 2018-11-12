"""
    Module: Car
    Purpose: a struct like class, designed to hold information within the model
             about a specific Object in the real world, in this case it holds
             a vehicle number, Organization Name, and Lap times associated with
             the the vehicle.

    Depends On: N/A

"""





class Car():

    def __init__(self, ID, Org, CarNum):
        self.ID = ID
        self.OrgName = Org
        self.CarNum = CarNum

        self.LatestLapID = 0
        self.LapCount = 50
        self.LapList = [[0] * 5] * 50

    """
        Function: addLapTime
        Parameters: self, hours, minutes, seconds, milliseconds
        Return Value: N/A
        Purpose: appends a laptime to the current LapList of the Car, and then increments what the
                 next ID to be used for the next Lap that will be.
    
    """
    def addLapTime(self, hours, minutes, seconds, milliseconds):
        if(self.LatestLapID > 50):
            newLap = (self.getLatestLapID(), hours, minutes, seconds, milliseconds)
            self.LapList.append(newLap)
            self.LatestLapID += 1
            self.LapCount = len(self.LapList)
        else:
            newLap = (self.getLatestLapID(), hours, minutes, seconds, milliseconds)
            self.LapList.insert(self.LatestLapID, newLap)
            self.LatestLapID += 1
            self.LapCount = len(self.LapList)

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
        self.LapList[lapID] = (lapID, 0, 0, 0, 0)

    """
         Function: editLapTime
         Parameters: self, ID, Hours, minutes, seconds, milliseconds
         Return Value: N/A
         Purpose: edits the laptime at the index ID, by reassigning its ID, and lap data to
                  that specific item with the lapList. Used with the assumption a user wants
                  to delete a lap and then re-enter other data.

     """
    def editLapTime(self, ID, hours, minutes=0, seconds=0, milliseconds=0):
        if milliseconds:
            self.LapList[ID] = (ID, hours, minutes, seconds, milliseconds)
        elif milliseconds and seconds:
            self.LapList[ID] = (ID, hours, minutes, 0, 0)
        elif milliseconds and seconds and minutes:
            self.LapList[ID] = (ID, hours, 0, 0, 0)
        elif hours:
            self.LapList[ID] = (ID, hours, minutes, seconds, 0)



    """
         Function: getLatestLapID
         Parameters: self
         Return Value: LatestLapID(Int)
         Purpose: Returns an integer that would be the current ID suggested to be used
                  when adding Laps to the LapList.

     """
    def getLatestLapID(self):
        return self.LatestLapID

    """
         Function: getLapByID
         Parameters: self ID
         Return Value: copy of Lap, found by an Index ID
         Purpose: Returns a copy of the Lap found at the index ID, such that a user can have
                  access to a lap without worry of modifying its' contents.

     """
    def getLapByID(self, ID):
        newlist = self.LapList.copy()
        if(ID >= self.LapCount):
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
         Function: getOrg
         Parameters: self
         Return Value: self.OrgName
         Purpose: Returns the currently set OrgName, used as part of a search and ease of access

     """
    def getOrg(self):
        return self.OrgName

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

    def getLapStringByID(self, lapID):
        tempLap = self.getLapByID(lapID)
        return str(tempLap[1]) + ":" + str(tempLap[2]) + ":" + str(tempLap[3])





#from src.table.LapTime import LapTime

import re

class Car():

    def __init__(self, ID, Org, CarNum):


        self.ID = ID
        self.OrgName = Org
        self.CarNum = CarNum

        self.LatestLapID = 0
        self.LapList = []


    def addLapTime(self, hours, minutes, seconds, milliseconds):
        newLap = (self.getLatestLapID(), hours, minutes, seconds, milliseconds)
        self.LapList.append(newLap)
        self.LatestLapID += 1

    def removeLapTime(self, lapID):
        self.LapList[lapID] = (lapID, 0, 0, 0, 0)

    def editLapTime(self, ID, hours, minutes, seconds, milliseconds):
        self.LapList[ID] = (ID, hours, minutes, seconds, milliseconds)

    def getLatestLapID(self):
        return self.LatestLapID

    def getLapByID(self, ID):
        newlist = list(self.LapList)
        return newlist[ID]

    def getCarID(self):
        return self.ID

    def getOrg(self):
        return self.OrgName

    def getCarNum(self):
        return self.CarNum








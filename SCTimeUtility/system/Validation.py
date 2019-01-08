'''
Module: Validation.py
Purpose: assortment of functions used to validate data before it is used for certain objects.

'''

import re, os
from SCTimeUtility.log.Log import getLog

RegExpID = "^([0-9][0-9]{0,2}|1000)$"
RegExpTeamName = "^[a-zA-Z]+(?:[\s-][a-zA-Z]+)*$"
RegExpCarNum = "^(?:500|[1-9]?[0-9])$"
RegExpFileName = "^[a-zA-Z0-9](?[a-zA-Z0-9 ._-]*[a-zA-Z0-9])?\.[a-zA-Z0-9_-]+$"

"""

    Function: isValidFilename
    Parameters: regExpFileName, filename 
    Return Value: Boolean indicator
    Purpose: Boolean check if given parameter filename matches the regular expression.

"""


def isValidPath(path):
    return os.path.exists(path)


"""

    Function: isValidFilename
    Parameters: regExpFileName, filename 
    Return Value: Boolean indicator
    Purpose: Boolean check if given parameter filename matches the regular expression.

"""


def isValidFilename(regExpFileName, filename):
    return re.findall(regExpFileName, filename)


"""

    Function: isValidElapsedTime
    Parameters: inputTime, totalCurrentTime
    Return Value: Boolean indicator
    Purpose: Boolean check if given parameter inputTime doesn't go past the total amount of time that
             has occurred.

"""


def isValidElaspedTime(inputTime, totalCurrentTime):
    return inputTime >= totalCurrentTime


"""

    Function: checkString
    Parameters: regExpTeamName, teamName
    Return Value: Boolean indicator
    Purpose: Boolean check if given parameter teamName matches regexp given which checks the name of the team.

"""


def isValidTeamName(regExpTeamName, teamName):
    check = False
    if type(teamName) is str:
        if re.findall(regExpTeamName, teamName):
            check = True
    return check


"""
    Function: checkNumRange
    Parameters: carNum, ExpCarNum
    Return Value: boolean indicator
    Purpose: Boolean check if given parameter carNum matches regexp given which checks the range of the carNum

"""


def isValidInteger(carNum, ExpCarNum):
    check = False
    if (type(carNum) is int):
        if (carNum > 0):
            if re.findall(ExpCarNum, str(carNum)):
                check = True

    return check


"""
    Function: carNumberExists
    Parameters: num, storageList
    Return Value: boolean indicator
    Purpose: Boolean check if the given parameter num, matches an existing carNum.

"""


def existsCarNumber(num, storageList):
    check = False
    for item in storageList:
        if item.getCarNum() == num:
            check = True
    return check


"""
    Function: teamNameExists
    Parameters: teamName, StorageList
    Return Value: boolean indicator
    Purpose: used as a form of validation to check if the given parameter exists or not.

"""


def existsTeamName(teamName, storageList):
    check = False
    for item in storageList:
        if item.getTeam() == teamName:
            check = True
    return check


"""
    Function: existsCar
    Parameters: teamName, StorageList
    Return Value: boolean indicator
    Purpose: used as a form of validation to check if the given parameters do or do not exist already within
             another car's variables.

"""


def existsCar(storageList, num, org):
    return existsCarNumber(num, storageList) or existsTeamName(org, storageList)


"""
    Function: isValidCar
    Parameters: num, teamName
    Return Value: boolean indicator
    Purpose: used as a form of validation to check if the given parameters are valid before car creation. 

"""


def isValidCar(num, teamName):
    return isValidInteger(num, RegExpCarNum) and isValidTeamName(teamName, RegExpTeamName)


"""
    Function: intToTimeStr
    Parameters: int
    Return Value: str
    Purpose: converts an integeter that represents milliseconds into a time string in the format "HH:MM:SS"

"""


def intToTimeStr(int):
    Days = divmod(int, 24 * 3600)
    Hours = divmod(Days[1], 3600)
    Minutes = divmod(Hours[1], 60)
    Seconds = divmod(int, 60)

    Hours = str(Hours[0])
    Minutes = str(Minutes[0])
    Seconds = str(Seconds[1])

    if len(Hours) == 1:
        Hours = '0' + Hours

    if len(Minutes) == 1:
        Minutes = '0' + Minutes

    if len(Seconds) == 1:
        Seconds = '0' + Seconds

    return Hours + ':' + Minutes + ":" + Seconds

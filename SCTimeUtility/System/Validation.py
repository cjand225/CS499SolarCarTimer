"""

    Module:
    Purpose:
    Depends On:

"""

import re

from SCTimeUtility.Log.Log import getLog

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

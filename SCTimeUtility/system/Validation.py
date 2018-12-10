'''
this is going to be used as a place for functions related to data validation
'''

from SCTimeUtility.log.Log import getInfoLog, getCriticalLog, getDebugLog, getErrorLog, getWarningLog

import re
import os

RegExpID = "^([0-9][0-9]{0,2}|1000)$"
RegExpOrg = "/^[a-z ,.'-]+$/i"
RegExpCarNum = "^(?:500|[1-9]?[0-9])$"
RegExpFileName = "^[a-zA-Z0-9](?[a-zA-Z0-9 ._-]*[a-zA-Z0-9])?\.[a-zA-Z0-9_-]+$"


def isValidFilePath(path):
    return os.path.exists(path)


def isValidFileName(fileName):
    return re.findall(RegExpFileName, fileName)


def isValidElaspedTime(inputTime, totalCurrentTime):
    if inputTime >= totalCurrentTime:
        return False
    else:
        return True


"""

    Function: checkString
    Parameters: self, orgName
    Return Value: orgName or Empty String
    Purpose: used as a form of validation to check if either the carNum matches the pattern used
             for Organization names. If there is no match, it'll return an empty string, else there is a 
             match and it returns the original parameter given.

"""


def isValidString(RegExpOrg, orgName):
    check = False
    if type(orgName) is str:
        if re.findall(RegExpOrg, orgName):
            check = True
    return check


"""
    Function: checkNumRange
    Parameters: self, carNum
    Return Value: -1 or carNumber
    Purpose: used as a form of validation to check if either the carNum matches either the pattern
             for IDs or the pattern for Vehicle Numbers before returning, if it doesn't it'll return
             a -1, meaning failure, or if it does, the actual number of the parameter, meaning a success

"""


def isValidInteger(carNum, ExpCarNum):
    check = False
    if (type(carNum) is int):
        if (carNum > 0):
            if re.findall(ExpCarNum, str(carNum)):
                check = True

    return check


# validation for existing cars
def carNumberExists(num, storageList):
    check = False
    for item in storageList:
        if item.getCarNum() == num:
            check = True

    return check


# validation for existing cars
def carOrgExists(org, storageList):
    check = False
    for item in storageList:
        if item.getTeam == org:
            check = True
    return check


def carExists(storageList, num, org):
    return carNumberExists(num, storageList) or carOrgExists(org, storageList)


def isValidCar(num, org):
    return isValidInteger(num, RegExpCarNum) and isValidString(org, RegExpOrg)


def intergerToTimeString(int):
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

'''
this is going to be used as a place for functions related to data validation
'''

from src.log.Log import getInfoLog, getCriticalLog, getDebugLog, getErrorLog, getWarningLog

import re


def isValidFilePath(path):
    print("PH")


def isValidFileName(fileName):
    print("PH")


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
    if (type(orgName) is str):
        if re.findall(RegExpOrg, orgName):
            return True
    else:
        return False


"""
    Function: checkNumRange
    Parameters: self, carNum
    Return Value: -1 or carNumber
    Purpose: used as a form of validation to check if either the carNum matches either the pattern
             for IDs or the pattern for Vehicle Numbers before returning, if it doesn't it'll return
             a -1, meaning failure, or if it does, the actual number of the parameter, meaning a success

"""


def isValidInteger(carNum, RegExpCarNum, RegExpID):
    if (type(carNum) is int):
        if (carNum > 0):
            if (re.findall(RegExpCarNum, str(carNum)) or re.findall(RegExpID, str(carNum))):
                return True
            else:
                return False
        else:
            return False
    else:
        return False

"""

    Module:
    Purpose:
    Depends On:

"""

import re

from SCTimeUtility.Log.Log import get_log

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


def is_valid_filename(reg_exp, filename):
    return re.findall(reg_exp, filename)


"""

    Function: isValidElapsedTime
    Parameters: inputTime, totalCurrentTime
    Return Value: Boolean indicator
    Purpose: Boolean check if given parameter inputTime doesn't go past the total amount of time that
             has occurred.

"""


def is_valid_elapsed_time(input_time, total_time):
    return input_time >= total_time


"""

    Function: checkString
    Parameters: regExpTeamName, teamName
    Return Value: Boolean indicator
    Purpose: Boolean check if given parameter teamName matches regexp given which checks the name of the team.

"""


def is_valid_team_name(reg_exp, team_name):
    return re.findall(reg_exp, team_name)


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


def car_number_exists(num, storageList):
    for item in storageList:
        if item.getCarNum() == num:
            return True
    return False


"""
    Function: teamNameExists
    Parameters: teamName, StorageList
    Return Value: boolean indicator
    Purpose: used as a form of validation to check if the given parameter exists or not.

"""


def team_name_exists(teamName, storageList):
    for item in storageList:
        if item.getTeam() == teamName:
            return True
    return False


"""
    Function: existsCar
    Parameters: teamName, StorageList
    Return Value: boolean indicator
    Purpose: used as a form of validation to check if the given parameters do or do not exist already within
             another car's variables.

"""


def car_exists(storage_list, car_number, team_name):
    return car_number_exists(car_number, storage_list) or team_name_exists(team_name, storage_list)


"""
    Function: isValidCar
    Parameters: num, teamName
    Return Value: boolean indicator
    Purpose: used as a form of validation to check if the given parameters are valid before car creation. 

"""


def is_valid_car(num, teamName):
    return isValidInteger(num, RegExpCarNum) and is_valid_team_name(teamName, RegExpTeamName)

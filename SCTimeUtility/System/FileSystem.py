"""

    Module:
    Purpose:
    Depends On:

"""

# Standard lib imports
import os, csv, datetime

'''  
    Function: importCSV
    Parameters: path (str)
    Return Value: List with CSV contents
    Purpose: parses and imports data from a directory containing CSVs.
'''

#TODO
def importCSV(path):
    if os.path.exists(path):
        pass
    else:
        pass


'''
    Function: exportCSV
    Parameters: path, carStorage
    Return Value: N/A
    Purpose: Exports every car in CarStorage instance to timestamped directory with each csv file being comprised
             of the car name, a dash, teamName, and the csv file extension inside the directory.

'''


def exportCSV(carStorage, path):
    folderPath = os.path.join(path, datetime.datetime.now().strftime('%Y-%b-%d_%H%M'))
    # if the timestamped folder doesn't exist, create it now
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)
    # go through each car and write it out to a csv file named after carNum-TeamName.csv
    for car in carStorage.storageList:
        fileName = str(car.CarNum) + '-' + str(car.TeamName) + '.csv'
        filePath = os.path.join(folderPath, fileName)
        with open(filePath, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Lap', 'Elapsed Time', 'First Edit', 'Last Edit', 'Time of Day'])
            lapCount = 0
            for lap in car.lapList:
                writer.writerow([lapCount, lap, lap.initialWrite, lap.lastWrite, lap.initialWrite.strftime("%I:%M")])
                lapCount += 1

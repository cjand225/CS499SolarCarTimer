import os, csv, datetime

'''  
    Function: importCSV
    Parameters: path (str)
    Return Value: List with CSV contents
    Purpose: parses and imports data from a directory containing CSVs.
'''


def importCSV(path):
    if os.path.exists(path):
        pass
    else:
        pass


'''
    Function: exportCSV
    Parameters: path, carStorage
    Return Value: Boolean Condition
    Purpose: Exports every car in CarStorage instance to timestamped directory with each csv file being comprised
             of the car name, a dash, teamName, and the csv file extension inside the directory.

'''


def exportCSV(carStorage, path):
    folderPath = os.path.join(path, datetime.datetime.now().strftime('%Y-%b-%d_%H%M'))
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)
    for car in carStorage.storageList:
        fileName = str(car.CarNum) + '-' + str(car.TeamName) + '.csv'
        filePath = os.path.join(folderPath, fileName)
        with open(filePath, 'w', newline='') as f:
            writer = csv.writer(f)
            for lap in car.LapList:
                writer.writerow([lap])

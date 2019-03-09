import os, csv, datetime

'''  
    Function: createFile
    Parameters: path (str), args (str)
    Return Value: 
    Purpose: Creates a file with provided path and arguments.
'''


def createFile(path, arg, data):
    if not os.path.isfile(path):
        fp = open(path, arg)
        for dataLine in data:
            if arg == "w":
                fp.write(dataLine)
            else:
                fp.read(dataLine)
        fp.close()


'''  
    Function: importCSV
    Parameters: path (str)
    Return Value: List with CSV contents
    Purpose: Imports the file given by the path parameter of a CSV and returns it as a list.
'''


def importCSV(path):
    if os.path.isfile(path):
        csvList = []
        with open(path, newline='') as csvFile:
            csvReader = csv.reader(csvFile, delimiter=' ', quotechar='|')
            for row in csvReader:
                csvList.append(row)
        return csvList
    else:
        return None


'''
    Function: exportCSV
    Parameters: path, carStorage
    Return Value: Boolean Condition
    Purpose: Exports every car in CarStorage instance to timestamped directory with each csv file being comprised
             of the car name, a dash, teamName, and the csv file extension inside the directory.

'''


def exportCSV(carStorage, path):
    # print(path)
    folderPath = os.path.join(path, datetime.datetime.now().strftime('%Y-%b-%d_%H%M'))
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)
    # print(folderPath)
    for car in carStorage.storageList:
        fileName = str(car.CarNum) + '-' + str(car.TeamName) + '.csv'
        filePath = os.path.join(folderPath, fileName)
        with open(filePath, 'w', newline='') as f:
            writer = csv.writer(f)
            for lap in car.LapList:
                writer.writerow([lap])

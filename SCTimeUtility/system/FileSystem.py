import os, csv

'''  
    Function: makeDir
    Parameters: dirName
    Return Value: Boolean cond
    Purpose: Checks if the logging path exists and if not makes the directory to complete the path.
'''


def makeDir(dirName):
    if not os.path.exists(dirName):
        os.makedirs(dirName)
    return True


'''  
    Function: dirExists
    Parameters: dirName (str)
    Return Value: Boolean cond
    Purpose: Returns a boolean cond that determines whether a directory exists or not.
'''


def dirExists(dirName):
    return os.path.exists(dirName)


'''  
    Function: fileExists
    Parameters: path (str)
    Return Value: Boolean cond
    Purpose: Returns a boolean cond that determines whether a file exists or not.
'''


def fileExists(path):
    return os.path.isfile(path)


'''  
    Function: createFile
    Parameters: path (str), args (str)
    Return Value: 
    Purpose: Creates a file with provided path and arguments.
'''


def createFile(path, arg, data):
    if not fileExists(path):
        fp = open(path, arg)
        for dataLine in data:
            if arg == "w":
                fp.write(dataLine)
            else:
                fp.read(dataLine)
        fp.close()


'''  
    Function: exportImage
    Parameters: path (str), img (image file)
    Return Value: Boolean Cond
    Purpose: Exports a graph image from application to path given by user.
'''


def exportImage(path, img):
    print()


'''  
    Function: importCSV
    Parameters: path (str)
    Return Value: List with CSV contents
    Purpose: Imports the file given by the path parameter of a CSV and returns it as a list.
'''


def importCSV(path):
    if fileExists(path):
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
    Purpose: Exports CarStorage to a csv formatted file.


'''


def exportCSV(path, carStorage):
    if fileExists(path):
        with open(path, 'w', newline='') as f:
            writer = csv.writer(f)
            for car in carStorage.storageList:
                writer.writerow(car.ID)
                writer.writerow(car.TeamName)
                writer.writerow(car.CarNum)
                writer.writerow('\n')
                writer.writerows(car.LapList)
    else:
        return None


'''  
    Function: isFileExtension
    Parameters: path, extension (str, str)
    Return Value: Boolean Condition
    Purpose: Checks if a string/path has the correct file extension located in extensionList and returns boolean 
             condition based on outcome.
'''

# def isFileExtension(path, extensionList):

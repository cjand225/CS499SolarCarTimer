"""

    Module:
    Purpose:
    Depends On:

"""
import csv, os, pandas

from SCTimeUtility.Table.Car import Car
from SCTimeUtility.Table.CarStorage import CarStorage
from SCTimeUtility.Log.Log import get_log

'''  
    Function: saveCSV
    Parameters: cs, filePath
    Return Value: N/A
    Purpose: Receives an instance of carStorage and a file path in which to dump all the contents of every object
             within CarStorage instance.
'''


def save_csv(car_storage_object, file_path):
    # Save a CarStorage object to a CSV file.
    if file_path != '':
        with open(file_path, "w") as storageFile:
            storage_writer = csv.writer(storageFile)
            # storageWriter.writeHeaders(['Car ID', 'Team Name', 'Car Num', 'Lap Times'])
            storage_writer.writerows([[c.ID, c.TeamName, c.CarNum, c.initialTime] +
                                      [t.elapsedTime for t in c.lapList]
                                      for c in car_storage_object.storage_list])


'''  
    Function: loadCSV
    Parameters: filePath
    Return Value: List [car info]
    Purpose: Loads a file assumed to be CSV format, into a list that is returned to the invoker.
'''


def load_csv(file_path):
    if file_path != '':
        car_list = []
        with open(file_path, "r") as storageFile:
            storage_reader = csv.reader(storageFile)
            for row in storage_reader:
                car_index = int(row[0])
                team_name = row[1]
                car_number = int(row[2])
                initial_time = float(row[3])
                elapsed_times = [float(i) for i in row[4:]]
                new_car = Car(car_index, team_name, car_number)
                new_car.initialTime = initial_time
                for time in elapsed_times:
                    new_car.addLapTime(time)
                car_list.append(new_car)
        return car_list


def load_table():
    print("PH")


def save_table():
    print("PH")


def create_directory(directory_path):
    if not os.path.exists(directory_path):
        os.mkdir(directory_path)

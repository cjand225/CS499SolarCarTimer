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


# TODO
def import_csv(path):
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


def export_csv(car_storage, path):
    folder_path = os.path.join(path, datetime.datetime.now().strftime('%Y-%b-%d_%H%M'))
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    for car in car_storage.storage_list:
        file_name = str(car.CarNum) + '-' + str(car.TeamName) + '.csv'
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Lap', 'Elapsed Time', 'First Edit', 'Last Edit', 'Time of Day'])
            lap_count = 0
            for lap in car.lapList:
                writer.writerow([lap_count, lap, lap.initial_write, lap.last_write, lap.initial_write.strftime("%I:%M")])
                lap_count += 1

"""
    Module: CarStorage
    Purpose: A data structure model created to handle cars and their related functions
             such as IDs, Vehicle Numbers, Organization Names, and Laptimes all conveniently
             stored as more or less a two dimensional list

    Depends On: Car

"""

import copy, datetime

from PyQt5.QtCore import QObject, pyqtSignal

from SCTimeUtility.Table.Car import Car
from SCTimeUtility.Table.LapTime import LapTime
from SCTimeUtility.Log.Log import get_log


class CarStorage(QObject):
    dataModified = pyqtSignal(int, int)

    def __init__(self):
        super().__init__()
        self.logger = get_log()
        self.storage_list = []
        self.seed_value = None
        self.offset_time = None
        self.enable_offset = False

    """
          Function: setSeedValue
          Parameters: self, seedTime
          Return Value: N/A
          Purpose: Function that sets the Seed Value of Car Storage and then calls setSeeds to globally
                  set that value for each car.

    """

    def set_seed_value(self, seed_time):
        if not self.seed_value and len(self.storage_list) > 0:
            self.seed_value = seed_time
            self.set_individual_seeds()
            self.logger.info('[' + __name__ + ']' + 'Setting Seed Value for All Cars')

    """
          Function: setSeeds
          Parameters: self
          Return Value: N/A
          Purpose: Function that sets the Seed Value of each car with the value of the "Global" seedValue
                   that is stored within Car Storage.

    """

    def set_individual_seeds(self):
        for car in self.storage_list:
            car.set_seed_value(self.seed_value)

    """
          Function: setOffsetTime
          Parameters: self, cond
          Return Value: N/A
          Purpose: Function that offsets absolute times calculated for reporting the time of day.

    """

    def set_offset_time(self, offset):
        self.offset_time = offset

    """
          Function: enableOffsetTime
          Parameters: self, cond
          Return Value: N/A
          Purpose: Function that flags CarStorage to offset the time of all the cars to better fit
                   the Time supplied to it. (May be deprecated later.)

    """

    def enable_offset_time(self, enabled):
        self.enable_offset = enabled

    """
          Function: createCar
          Parameters: self, list
          Return Value: N/A
          Purpose: Goes through list parameter, checks if the first item is a digit. If so, it assumes
                   that is it the car number and creates that car with Item 0 as ID and Item 1 as Team Name,
                   otherwise it assumes Item 1 is ID and Item 0 is Team Name. Validation is done via
                   AddBatchDialog.

    """

    def create_car(self, car_number, team_name):
        new_car = Car(self.get_latest_car_id(), str(team_name), car_number)
        if self.seed_value is not None:
            new_car.setSeedValue(self.seed_value)
        self.storage_list.append(new_car)
        self.dataModified.emit(new_car.ID, 0)
        new_car.lapChanged.connect(lambda l: self.dataModified.emit(new_car.ID, l))
        self.logger.info('[' + __name__ + ']' + 'Adding Car: {} , {}'.format(team_name, car_number))

    """
          Function: createCars
          Parameters: self, list
          Return Value: N/A
          Purpose: Goes through list parameter, checks if the first item is a digit. If so, it assumes
                   that is it the car number and creates that car with Item 0 as ID and Item 1 as Team Name,
                   otherwise it assumes Item 1 is ID and Item 0 is Team Name. Validation is done via
                   AddBatchDialog.

    """

    def create_cars(self, car_list):
        index = 0
        for item in car_list:
            if len(item) == 2:
                self.create_car(item[1], item[0])
            index += 1

    """
         Function: removeCar
         Parameters: self, ID
         Return Value: N/A
         Purpose: Removes a car by its ID number within the list, from the view side, it'll likely
                  be the column number in which the car is placed. After removal, the list is then
                  re-indexed to its proper positions starting where the object was removed to the
                  end of the list, to allow for proper ID management.

    """

    def remove_car(self, ID):
        self.storage_list.remove(self.get_car_by_id(ID))
        self.sort_storage(ID)

    """
         Function: reindexStorage
         Parameters: self, ID
         Return Value: N/A
         Purpose: Reindexes the ID values of each car starting at the ID value given as a parameter,
                  used soley after a removal has been processed to prevent off by 1 errors or out of
                  bounds errors with the StorageList.

    """

    def sort_storage(self, ID):
        for x in range(ID, len(self.storage_list) - 1):
            self.storage_list[x].setID(x - 1)

    """
         Function: getCarByID
         Parameters: self, ID
         Return Value: Copy of Car at index ID
         Purpose: Used for getting a reference a copy of a specific car within carStorage, typically used
                  for easier access of each car without having to know specifically where its at
                  within carStorage w/ no intentions of altering the original car. Used only when index
                  Number is Known.

    """

    def get_car_by_id(self, ID):
        if ID in range(0, len(self.storage_list) - 1):
            return self.storage_list[ID]
        else:
            return False

    """
         Function: getCarByNum
         Parameters: carNum
         Return Value: copy of Car that contains value CarNum
         Purpose: Used for getting a reference to a copy of a specific car within carStorage, typically used
                  for easier access of each car without having to know specifically where its at
                  within carStorage w/ no intentions of altering the original car. Used when only Vehicle Number
                  is Known.

    """

    def get_car_by_car_number(self, car_number):
        for item in self.storage_list:
            if item.getCarNum() == car_number:
                return item

    """
         Function: getCarByTeamName
         Parameters: OrgString
         Return Value: copy of Car that contains value teamName
         Purpose:  Used for getting a reference to a copy of a specific car within carStorage, typically used
                  for easier access of each car without having to know specifically where its at
                  within carStorage w/ no intentions of altering the original car. Used when only Vehicle Organization
                  is Known.

    """

    def get_car_by_team_name(self, team_name):
        item_list = [item for item in self.storage_list if item.getTeam() == team_name]
        item = item_list[0]
        return item

    """
         Function: appendLapTime
         Parameters: CarID, Hours, Minutes, Seconds, Milliseconds
         Return Value: N/A
         Purpose: Given the CarID, this function will call addLap for the class Car at Index CarID,
                  which will then add the specific lap information to the specified car class given
                  from the parameters.

    """

    def append_lap_time(self, car_index, time):
        self.storage_list[car_index].addLapTime(time)

    """
         Function: editLapTime
         Parameters: CarID, LapID, Hours, Minutes, Seconds, Milliseconds
         Return Value: N/A
         Purpose: Given the CarID, this function will call editLap for the class Car at Index CarID,
                  which will then edit the specific lap information to the specified car class given
                  from the parameters.

    """

    def edit_lap_time(self, car_index, lap_index, hours, minutes, seconds, milliseconds):
        self.storage_list[car_index].edit_lap_time(lap_index, hours, minutes, seconds, milliseconds)

    """
         Function: removeLapTime
         Parameters: CarID, LapID
         Return Value: N/A
         Purpose: Given the CarID, this function will call removeLapTime for the class Car at Index CarID,
                  which will then add the specific lap information to the specified car class given
                  from the parameters.

    """

    def remove_lap_time(self, car_index, lap_index):
        self.get_car_by_id(car_index).removeLapTime(lap_index)

    """
         Function: getCarListCopy
         Parameters: self
         Return Value: copy of StorageList
         Purpose: Used for getting a copy of the model for usage within other modules within the Application
                  such as view components like graphing/TableView/etc.

    """

    def car_list_copy(self):
        storage_copy = []
        storage_copy.clear()
        for car in range(0, len(storage_copy) - 1):
            storage_copy.append(copy.deepcopy(self.storage_list[car]))
        return storage_copy

    """
         Function: getCarNames
         Parameters: self
         Return Value: list of Org names of all cars
         Purpose: Used as a convenient method for accessing all the cars' Team Name.

    """

    def car_names_copy(self):
        new_list = self.storage_list.copy()
        names = []
        for x in range(0, len(new_list)):
            names.append(new_list[x].getTeam())
        return names

    """
         Function: getLatestCarID
         Parameters: self
         Return Value: LatestCarID(int)
         Purpose: gives the next ID to be used, which is the length of the storageList

    """

    def get_latest_car_id(self):
        return len(self.storage_list)

    """
        
        Function: getCarCount
        Parameters: self
        Return Value: N/A
        Purpose: Used to find how many cars are stored within CarStorage
    
    """

    def get_car_count(self):
        return len(self.storage_list)

    """

        Function: getHighestLapCount
        Parameters: self
        Return Value: N/A
        Purpose: Used to find the highest amount of laps stored within all the cars in carStorage

    """

    def get_highest_lap_count(self):
        new_list = self.storage_list.copy()
        highest = 0
        for x in range(0, len(new_list)):
            if new_list[x].getLapCount() > highest:
                highest = new_list[x].getLapCount()
        return highest

    '''
        Function: startCar
        Parameters: self, index
        Return Value: N/A
        Purpose: Starts car given at index parameter, allowing for recording of time values.
    
    '''

    def start_car_by_index(self, index):
        if index in len(self.storage_list):
            # start
            if self.storage_list[index].hasSeed() and self.storage_list[index].is_running():
                self.storage_list[index].start()
            # start
            elif not self.storage_list[index].hasSeed():
                self.storage_list[index].set_seed_value()

    '''
        Function: startCar
        Parameters: self, index
        Return Value: N/A
        Purpose: Starts car given at index parameter, allowing for recording of time values.

    '''

    def stop_car_by_index(self, index):
        if index in len(self.storage_list):
            if self.storage_list[index].hasSeed() and self.storage_list[index].is_running():
                self.storage_list[index].stop()

    '''
        Function: startCar
        Parameters: self, index
        Return Value: N/A
        Purpose: Starts car given at index parameter, allowing for recording of time values.

    '''

    def start_all_cars(self):
        if isinstance(self.seed_value, datetime.datetime):
            for car in self.storage_list:
                car.set_seed_value(self.seed_value)
        elif not self.seed_value:
            self.seed_value = datetime.datetime.now()
            for car in self.storage_list:
                car.set_seed_value(self.seed_value)

    '''
        Function: stopCars
        Parameters: self, index
        Return Value: N/A
        Purpose: Starts car given at index parameter, allowing for recording of time values.

    '''

    def stop_all_cars(self):
        for car in self.storage_list:
            car.stop()

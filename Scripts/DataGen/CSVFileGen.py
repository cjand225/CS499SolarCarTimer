from Tests.DataGen.DataGeneration import *

import os, sys, time, csv

from SCTimeUtility.Table.Car import Car
from SCTimeUtility.Table.CarStorage import CarStorage
from SCTimeUtility.Table.LapTime import LapTime
from SCTimeUtility.System.FileSystem import *

storage = CarStorage()
populateStorage(200, storage)

for car in storage.storage_list:
    list = generateLapData(200)
    for lap in list:
        car.addLapTime(lap)



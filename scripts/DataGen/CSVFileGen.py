from tests.dataGen.DataGeneration import *

import os, sys, time, csv

from SCTimeUtility.table.Car import Car
from SCTimeUtility.table.CarStorage import CarStorage
from SCTimeUtility.table.LapTime import LapTime
from SCTimeUtility.system.FileSystem import *

storage = CarStorage()
populateStorage(200, storage)

for car in storage.storageList:
    list = generateLapData(200)
    for lap in list:
        car.addLapTime(lap)



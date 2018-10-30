'''
Module: App.py
Purpose: Controller for entire application, used to periodically update project with data to and from the
         modal.

'''

from PyQt5.QtCore import *


class App():

    def __init__(self):
        self.mainWindow = None

# SCTiming Utility

An application written in python to track lap times during solar car races. Tracking comes in three different modes: Manual Entry, Semi-Automatic, Automatic.

Each Mode is Performed by:
- Manual Entry - Keyboard input into spreadsheet
- Semi-Automatic - Button presses for each car
- Automatic - Computer Vision/Processing via Webcam

The application also has a built in graphing module that can create various graphs based on the existing car data as well as a Leaderboard that can track and compare each car against all other cars within the same race.


## Requirements

A virtual environment
(Not really necessary but good to have if you're working on seperate projects, this project was created using a Conda virtual environment.)

As well as the following packages w/ their version numbers.

    Packages:
        -numpy >= 1.15.4
        -matplotlib >= 2.2.3
        -PyQt5 >= 5.6.0
        -opencv-contrib-python >= 3.4.3
        -pywin32 >= 1.0; platform_system == "Windows"
        -tesseract >= 0.1.3

## Development

Project Development was done using conda virtual environments.

First:

    git clone https://github.com/deedlehof/CS499SolarCarTimer.git
    cd ./CS499SolarCarTimer



If you have Anaconda Package Manager installed and have your %PATH% env setup correctly.
(If you're not sure, be sure to use "Anaconda Prompt" which is provided with the installation of Anaconda3)
### Creating an Environment

#### Using pre-existing package list 

##### Windows

    conda create -n <name> --file Install\envBuild_Windows.txt
    
##### Linux

    conda create -n <name> --file Install\envBuild_Linux.txt
    
##### MacOS

    conda create -n <name> --file Install\envBuild_MacOS.txt

Activate the environment after creation:

    conda activate <name>
    
Running project from `terminal` or `command prompt`:

    python -m SCTimeUtility.__main__
    

_Note: All builds provided will only work on their respective 64-bit systems_

_(Env Build testing was performed on Ubuntu 18.04 and Windows 10 respectively.)_

#### Creating a Clean Environment

First, create the environment using:

    conda create -n <name>
    
Activate it using:

    conda activate <name>
    
Then install the packages (from the package list) using either `pip` or `conda`:

    conda install <package-name>
    pip install <package-name>
    
    
After installing all the required packages, run (in the project folder):

    python -m SCTimeUtility.__main__
    
_Note: If using conda to install packages, you may want to use [conda-forge](https://conda-forge.org) as the package provider._


## Installation

### Building from Source

To build the program package (depending on what platform you want):

Python Wheel (Cross-Platform):
    
    python setup.py -bdist_wheel

EXE (Windows):

    python setup.py -bdist_wininst

MSI (Windows):

    python setup.py -bdist_msi

RPM (Linux):

    python setup.py -bdist_rpm
    
### Pre-built Packages

Below are some pre-built packages provided for convenience if you'd prefer not to build the application yourself.
    
    
### Running Application
After the package has been built, just run:

If wheel (or wanting to run from `terminal or cmd`)

    python -m SCTimeUtility
    
Otherwise, Just use click the shortcut in either the start menu or desktop.

_note: shortcuts are currently a work in progress and will be implemented shortly(For now, just use the command above after installing)_

	
# Authors and license

Licensed under GNU General Public License v3.0

Package was designed and written by:
- [@cjand225](https://github.com/cjand225) 
- [@deedlehof](https://github.com/deedlehof)
- [@actapia](https://github.com/actapia)   
- [@Pback9](https://github.com/Pback9)


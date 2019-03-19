# SCTimeUtility

## Overview 
Python application created to track lap times during solar car races. 
Tracking can be accomplished with 3 different modes: Manual Entry, Semi-Automatic, Automatic.

Each Mode is Performed by:
- Manual Entry - Excel-like Spreadsheet Table
- Semi-Automatic - Button Widget that handles Recording, Starting/Stopping of Cars, etc.
- Automatic - Object Recognition system for detecting cars via webcam feed.

Also comes with Graphing and LeaderBoard Modules used to track and analyze car data.

## Requirements

A virtual environment.

As well as the following packages w/ their version numbers.

    Packages:
        -numpy >= 1.15.4
        -matplotlib >= 2.2.3
        -PyQt5 >= 5.6.0
        -opencv-contrib-python >= 3.4.3
        -pywin32 >= 1.0; platform_system == "Windows"

## Development

Refer to Admin Manual under Resources/Docs in package.

## Installation

### Pre-built Packages

Check here for pre-build releases:

[Latest Release](https://github.com/cjand225/SCTimingUtility/releases/latest)

### Building from Source

To build the program package (depending on what platform you want):

Python Wheel (Universal):
    
    python setup.py -bdist_wheel

EXE (Windows):

    python setup.py -bdist_wininst

MSI (Windows):

    python setup.py -bdist_msi

RPM (Linux):

    python setup.py -bdist_rpm
    

### Running Application
After the package has been built and installed via pip, just run:

    python -m SCTimeUtility
    
	
# Authors and license

Licensed under GNU General Public License v3.0

Package was designed and written by:
- [@cjand225](https://github.com/cjand225) 
- [@deedlehof](https://github.com/deedlehof)
- [@actapia](https://github.com/actapia)   
- [@Pback9](https://github.com/Pback9)


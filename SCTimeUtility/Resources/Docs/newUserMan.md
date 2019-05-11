#User Manual

## Table of Contents
1. [Overview](#overview)
2. [Setup](#setup)
3. [Car Dynamics](#car-dynamics)
    * [Add](#add)
    * [Remove](#remove)
    * [Edit](#edit)
4. [Recording Methods](#recording-methods)
5. [Data Management](#data-management)
6. [Extra Comments](#extra-comments)

## Overview

The SCTimeUtility was created with the purpose of recording lap-times for races and practice runs. 
It has a variety of recording methods, with a custom "car" backend which keeps track of all the timing data. 

The program itself is build mostly from PyQt, Matplotlib, numpy, and Pandas.

## Setup

### Binary

### Package

## Car Dynamics

### Add

Adding a car can be done by either double clicking the left most column on the table, or by using the add car button.

Both will be displayed in the images below.



### Remove

Removing a car can be done by using the delete car button as seen below.


### Edit

Editing a car can be done by using the Edit Car button as seen below.

## Recording Methods

### Manual

Manual Entry is done by inputting data into the cell of any previously filled cell or the next empty row.

You can edit times by inputting times into an existing row's time, as well as add new times on the next most empty row cell.

### Semi-Auto

Semi-Automatic entry of lap-times are performed by the Semi-Auto widget. 

The widget has individual controls for each car added to the current session.

These controls allow the user to Start, Stop, Record, and Predict lap-times for the corresponding car as displayed below.


### Auto

Automatic entry is handled via the Auto Widget.

This widget is an interface for automatic detection of car numbers by use of machine learning and a motion-detection system
that is given raw frames from a webcam feed.

Once the user starts this mode, automatic recording of times will happen whenever a detection is found to have occurred.

_Note: This mode is currently in development and is not fit for use._

## Data Management

### Import

Importing data is performed via File -> Import. 

It will only read CSV files from a directory and import them
based on the filename as the car name and car number and the file's contents as the laptimes.

### Export

Exporting Data is performed via File -> Export

This exports all table data to a given location in CSV formats with the filenames being a concatenation of 
both the team name and car number, allowing for ease of use of individual car data.


## Extra Comments

Things that don't involve the above will be put here until there is a more defined category for them.
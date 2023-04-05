# Rebalancer #
### Purpose of this Project ###
The goal of this project was to automate, as much as possible, the rebalancing process from a fund management perspective. 
There was several important boundaries to establish. Reading data from Horizon or using the Morningstar API were ruled out. 
This is due to cost concerns, as well as the permissions required for this level of access.

### Structure ###
This folder contains the necessary project files, as well as a list of rebalancers that've been tested. There is also a 
folder that also contains populated rebalancers that demonstrate the suggested trades. Completed rebalancers will also
contain a sheet that contains a list of trades in the same format as the Fund Managers .csv file.

Instructions for this program can be found in the [instructions](INSTRUCTIONS.pdf) document.
Condensed instructions can be found in the [Execution Instuctions](Execution%20Instructions.pdf)

This Python project has been broken into several, smaller Python files. This is to increase the ease with which the
document can be read.

This is achieved, by giving each overarching function of the project, its own python document.

The constants document finds all fixed points within each rebelancer file. i.e. start and end points of the funds,
the equity & bonds sectors and the cash cell, etc.

The file ID reader prompts the user for the file(s) that they want to be read.

Following input from ops and dealing, functions have been added to allow for intelligent generation of filenames,
as well as finding the Scheme Identifier from the 'Constants/scheme_list_desig.xlsx' spreadsheet.
If the designation is not found, steps should be taken to ensure the 
[Scheme List]("X:\Fund Management\Fund Management Team Files\Richard\scheme_list_desig.xlsx") document 
is structured correctly. 

### Individual Files and their purpose ###
#### Rebalancer ####
This file does the rebalancing within the project. It reads tolerances for funds from constants. 
This enables the file to be strictly focused on rebalancing and the mathmatics involves. 
Furthermore, it makes use of several other documents to reduce the size, and bloat of the file. 

####Trade Reader ####
This program is designed to read from a completed rebalancer and generate a sheet that can be passed into Horizon. 
The purpose of this program is to enable trades to be passed into Horizon with as little manual entry as possible. 
This functionality is built into the Rebalancer, but whilst that is still in development, there is a need for this program. 

#### Trade Writer ####
This program holds some functionality that is to be used in the rebalancer. This reduces code bloat in the rebalancer. 
It also allows some functions to be used by the Trade Reader while the rebalancer is under development. 

#### Constants ####
This document holds and calculates all fixed points within a rebalancer (fund start and end points, the cash cell, etc.)
This code is to be run once per document read, as a result, due to this being used in both major functions of this project
adding it to an independent file reduced the amount of duplicated code. 

#### File ID Reader #### 
This file was generated, because these functions are run for both functions of this project. 
As a result, having this written once, and able to be referenced from various files, saved repeating code chunks. 


### Fund managers and their dealing codes ### 
Liz: ELIZABETH  
Dmitry: DMITRY  
Richard Cole: FMONEY  
Wayne: OPES  
IBOSS: IBOSS  
SENTINEL: SENTINEL  
CLARION: CLARION (This actually returns Liz as the fund manager, but changes notes to say 'Clarion Instructed')


### Trade Reading ###
Trade reading will take completed rebalancer documents and generate a document for automated trading. 

The files used by the trade reading function are: 
- trade_reader.py
- trade_writer.py
- file_id_reader.py
- constants.py

For this to work correctly there needs to be completed rebalancers in the root directory, and no other .xlsx files.
Blank rebalancers, or other .xlsx files will return a skewed output. 
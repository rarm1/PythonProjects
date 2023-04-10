# Instructions #

In order to run the trade reader, there are some prerequisites that must be fufilled.

## Opening Command Prompt ##

First open 'Command Prompt'. This can either be done by searching in the Windows menu bar, or
by pressing ctrl+r and entering 'cmd' in the Run window. Once this window is open:

<img alt="img.png" height="450" src="img.png" width="750"/>

## Install Python ##

To do this type 'python' in the window. If Python is not installed then it will open 'Microsoft Store' and direct the
window
to the Python download screen. If you are not confident with this, or have never used Python before,
this can be done under the supervision of the IT department. However, as long as these instructions
are not deviated from, this is a matter of preference, not necessity.

<img alt="img_1.png" height="450" src="img_1.png" width="800"/>

Once this is installed. Enter 'python' in the console. That will run Python.

<img alt="img_2.png" height="450" src="img_2.png" width="750"/>

Python can then be exited by entering 'ctrl+z' then enter.

### Install Required Packages ###

This program has multiple dependancies to run effectively.
To install these dependancies, the following code can be run in the Command Prompt.
This can either be copy and pasted in one block, or entered line by line.

```commandline
pip install --upgrade pip
pip install sys
pip install os
pip install pandas
pip install datetime
pip install openpyxl
```

## Get to the correct directory ##

The trade writer has been placed in a central location on the X: drive.
To get to the location enter the following in console:

```commandline
X:
cd X:\Fund Management\Fund Management Team Files\Richard\Trade Reader

```

## Running the program ##

To start the program, enter:

```commandline
python trade_reader.py
```

This will run the trade reader immediately and prompt the user for various inputs:
First: The Fund Manager.
Secondly: The file(s) to be read.

### Tidy Trades Sheet ###

When the trades have been read, there are two columns that must be deleted from the completed sheet.
The values cannot be deleted - both columns must be selected, then right-clicked and then deleted.
Otherwise, when they are passed into Horizon, they will generate errors.

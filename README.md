# Chess Tournaments Manager

> ### ***Disclaimer :***
> *This project, including what is included in this README, is a school project responding to a 
> fictional scenario and has no other purpose.*  

A little CLI program written in Python in order to manage chess tournaments.

## Installation

The application itself does not require any prerequisites and currently works well with Python's 
standard library. However, the installation of *flake8-html* is necessary if you want to generate 
a flake8 report in html (this will be detailed later).  
Thus, in the specific case of this school project, a file 'requirements.txt' has been added but 
currently only containing *flake8-html*, a simple direct installation is also possible. So:
```bash
pip install -r requirements.txt
```
or:  
```bash
pip install flake8-html
```

I recommend to do this in a fresh virtual environment. If you need a reminder on how to set up a 
virtual environment using venv, you can find the documentation [here](https://docs.python.org/3/library/venv.html).  

*Developed and tested under Python 3.11.2*

## Usage

Simply use Python to execute ***ChessApp.py*** in your terminal as usual.  
Navigate the menus and use the application by typing corresponding inputs.  

Datas is handled as **json** files in a local folder named ***datas***. *players.json* contains our 
players base and *tournaments.json* contains tournaments' related data. Before being modified, saves 
are made, and you can find them as .bak if needed.

## Flake8 report

Flake8 options have been configured in the *setup.cfg* file at the root of the project. To generate 
the report, simply execute flake8 in your terminal, being placed in the root of the project:
```bash
flake8
```
The report will be generated in the folder ***flake8_rapport*** as an ***index.html*** file and so 
is readable through any standard web browser.

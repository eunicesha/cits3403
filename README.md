# Roshambo'd ✊✌️✋
CITS3403 S1 2024 Group Project

## About
Welcome to Roshambo'd, where you can play paper scissors rock against other users! 

Users create an account and compete against others, where they gain a point for every win and lose one for every loss. 
You can iniate games, or respond to ones created by other users.

You can see your history - game records are displayed on the profile page- and know if you are beating your friends with 
the leaderboard page! 

Users can also customise their accounts with username changes, or adding a personal description in the 'about me' section.

---
## Credit
    __UWA ID__      ||  __NAME__            ||  __GITHUB USERNAME__   
    23451626    ||  DAVIN DO        ||  RUBBADUK
    23729581    ||  MIA O'DEA       ||  MIA-ODEA
    23671856    ||  HOIYEN SHA      ||  EUNICESHA
    24388802    ||  TASHI LHAMO     ||  TA-SHII

---
## Launching
### Prerequisites
[//]: # (Should check what version of python is actually needed)
This project requires a minimum of python 3.10, which can be downloaded using the following instructions:
#### linux:
```
$ sudo apt-get install python3.10
```
#### mac:
```
$ brew install python3
```
#### windows:
Download the installer from the [python website](https://www.python.org/downloads/windows/)

### Installation
A virtual environment must be set up using the terminal in the root directory of the project.
#### mac and Linux:
```
$ python3 -m venv flask
$ source flask/bin/activate
$ pip install -r requirements_unix.txt
```
#### windows
```
python -m venv flask
.\flask\Scripts\Activate.ps1
pip install -r requirements_unix.txt
```
If an error occurs, run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process` in Powershell.

## Running the Tests
** If the virtual environment is active when the tests are run, there will be an error**
The tests are run by executing the following command using terminal in the root directory of the project.
```
python3 -m tests
```
AND
```
python3 -m selenium_test
```
[//]: # (or whatever the selenium test is actually called)

## Deployment
The website can be deployed using terminal in the root directory of the project:
```
flask run
```
OR
```
python3 -m flask run
```
---
## In Depth Description
Roshambo'd! is an online game, based on the idea of a classic paper, scissors,
rock game. Users will first be prompted to sign in, or register for an account
if they don't already have one.
Upon signing in, the user is greeted by a quick description and guide of the game. The main purpose of the website is then shown; a screen of 'challenges' will be presented, either showing 'no games have been created', or 'challenge cards' that have been created by other users. Users can then 'accept' another users challenge, or create their own.
This is where an list of options are presented: paper, scissors, or rock. Submitting one own's challenge will create their own challenge card for others to see, otherwise submitting an option against someone else's challenge will determine a winner/loser (based on paper beats rock, rock beats scissors, etc).
The winner will then be granted a point, with the loser having a point deducted.
Our website also features a leaderboard and a profile section. The leaderboard will present all users, ordered by their respective points.
The profile section showcases the user's name, points, image, last login details and a record of their past games. There is also an option to edit their profile, changing their username, or adding an optional 'about me' text.
Users can also log out, prompting them to the sign-in page again.

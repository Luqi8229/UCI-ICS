ICS32 Assignment 2: Journal

This assignment includes the following starter files:

a2.py : Use this file as the main module for your program.
input_processor.py : Use this file for your user interface module.
Profile.py : Use this file to manage saving and loading of user data. Do not edit.

Please visit the course Canvas for a detailed overview of the assignment.

Luqi's notes
a2.py is the main python file for the group of python codes.
-enter "admin" when prompted to disable input messages but it would still allow printed messages like menu and confirmation messages
-some commands are extended from a1.py
-input is flexible when not in admin mode.
  -"L [DIR] -r" would work
  -"L" would also work but the code would just prompt helpful input messages like "Please enter specific directory" after "L"
-admin mode is expected to write commands perfectly; without missing required inputs
-"Q" is only allowed when asked for main command. Entering "Q" while in another command, like "C" would not work

DSU File:
-Suggestion to create a file will arise when File does not exist during O command but not create it.
  -same for L
  -code will continuously prompt for valid directory
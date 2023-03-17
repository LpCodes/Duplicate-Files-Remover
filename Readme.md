# Duplicate File Remover

This Python script removes duplicate files from a given directory. It prompts the user to select a folder and then uses the MD5 hashing algorithm to check if any files have the same hash value. If it finds duplicate files, it deletes all but one of them.

## Requirements

Python 3.x
tkinter module
pathlib module

## Installation

Clone this repository or download the duplicate_file_remover.py file.
Install the required modules by running pip install tkinter pathlib in your terminal.

## How to Use

Open your terminal or command prompt and navigate to the directory where you saved duplicate_file_remover.py.
Run the script by entering python ```duplicate_file_remover.py```

A dialog box will appear asking you to select a folder. Choose the folder containing the files you want to remove duplicates from.
The script will then loop through all files in the folder, calculate their MD5 hash values, and keep track of unique files.
If it finds duplicate files, it will print a message to the console and delete all but one of the duplicates.

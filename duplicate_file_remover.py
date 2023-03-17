from tkinter import Tk
from tkinter.filedialog import askdirectory
import os
import hashlib
from pathlib import Path


def calculate_hash(file_name):
    with open(file_name, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()


def is_file(file_name):
    return Path(file_name).is_file()


def delete_duplicate_files(path):
    files_list = [os.path.join(path, file) for file in os.listdir(path)]
    unique = {}
    for file_name in files_list:
        if is_file(file_name):
            file_hash = calculate_hash(file_name)
            if file_hash not in unique:
                unique[file_hash] = file_name
            else:
                print(f"Deleting duplicate file: {file_name}")
                os.remove(file_name)


if __name__ == '__main__':
    Tk().withdraw()
    path = askdirectory(title='Select Folder')
    if not os.path.exists(path):
        raise Exception("Path does not exist")
    delete_duplicate_files(path)

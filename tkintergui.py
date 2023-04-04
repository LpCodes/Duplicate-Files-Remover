import os
import hashlib
import tkinter as tk
from tkinter import filedialog, messagebox


def browse_folder():
    folder_selected = filedialog.askdirectory()
    folder_path.set(folder_selected)


def search_duplicates():
    folder_path_str = folder_path.get()
    if not folder_path_str:
        messagebox.showwarning("Warning", "Please select a folder to search.")
        return

    file_list.delete(0, tk.END)
    status_label.config(text="Searching for duplicates...")

    file_sizes = {}
    file_hashes = {}

    for root_folder, _, files in os.walk(folder_path_str):
        for file in files:
            file_path = os.path.join(root_folder, file)
            file_size = os.path.getsize(file_path)

            if file_size not in file_sizes:
                file_sizes[file_size] = [file_path]
            else:
                file_sizes[file_size].append(file_path)

    for file_size, file_paths in file_sizes.items():
        if len(file_paths) > 1:
            for file_path in file_paths:
                with open(file_path, "rb") as f:
                    file_hash = hashlib.md5(f.read()).hexdigest()

                if file_hash not in file_hashes:
                    file_hashes[file_hash] = [file_path]
                else:
                    file_hashes[file_hash].append(file_path)

    for file_hash, file_paths in file_hashes.items():
        if len(file_paths) > 1:
            for file_path in file_paths:
                file_list.insert(tk.END, file_path)

    status_label.config(text=f"Found {len(file_hashes)} duplicates.")


def remove_duplicates():
    items = file_list.curselection()
    if not items:
        messagebox.showwarning("Warning", "Please select files to remove.")
        return

    confirmed = messagebox.askyesno("Confirmation", "Are you sure you want to remove selected files?")
    if not confirmed:
        return

    for index in items:
        file_path = file_list.get(index)
        os.remove(file_path)
        file_list.delete(index)

    status_label.config(text="Selected files removed.")


def remove_all_duplicates():
    confirmed = messagebox.askyesno("Confirmation", "Are you sure you want to remove all duplicates?")
    if not confirmed:
        return

    items = file_list.get(0, tk.END)
    for file_path in items:
        os.remove(file_path)

    file_list.delete(0, tk.END)
    status_label.config(text="All duplicates removed.")


root = tk.Tk()
root.title("Duplicate File Finder")

label1 = tk.Label(root, text="Select a folder to search:")
label1.pack()

folder_path = tk.StringVar()
folder_entry = tk.Entry(root, textvariable=folder_path, width=40)
folder_entry.pack(side=tk.LEFT)

browse_button = tk.Button(root, text="Browse", command=browse_folder)
browse_button.pack(side=tk.LEFT)

search_button = tk.Button(root, text="Search for Duplicates", command=search_duplicates)
search_button.pack(pady=10)

remove_button = tk.Button(root, text="Remove Selected Duplicates", command=remove_duplicates)
remove_button.pack(pady=10)

remove_all_button = tk.Button(root, text="Remove All Duplicates", command=remove_all_duplicates)
remove_all_button.pack(pady=10)

file_list = tk.Listbox(root, width=80, height=20)
file_list.pack()

status_label = tk.Label(root, text="")
status_label.pack(pady=10)

root.mainloop()

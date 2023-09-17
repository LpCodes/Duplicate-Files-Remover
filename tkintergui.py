import hashlib
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

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

    if len(file_hashes) == 0:
        messagebox.showinfo("No Duplicates Found", "No duplicate files were found in the selected folder.")
        status_label.config(text="No duplicates found.")
    else:
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

    for index in reversed(items):  # Reverse the list to avoid index issues when deleting
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
root.geometry("900x500")

# change the theme to 'clam'
style = ttk.Style()
style.theme_use('clam')

# create a style for the GUI
style.configure("TButton", font=("Helvetica", 14), foreground="white", background="#4CAF50", pady=10, padx=20)
style.configure("TLabel", font=("Helvetica", 14), foreground="#333", pady=8)
style.configure("TEntry", font=("Helvetica", 14), pady=8, padx=10)
style.configure("TListbox", font=("Helvetica", 14), pady=8, padx=10)
style.configure("TFrame", background="#f8f9fa")

# create a frame to contain all the widgets
frame = ttk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

label1 = ttk.Label(frame, text="Select a folder to search:")
label1.pack()

folder_path = tk.StringVar()
folder_entry = ttk.Entry(frame, textvariable=folder_path, width=40)
folder_entry.pack(side=tk.LEFT)

browse_button = ttk.Button(frame, text="Browse", command=browse_folder)
browse_button.pack(side=tk.LEFT)

search_button = ttk.Button(frame, text="Search for Duplicates", command=search_duplicates)
search_button.pack(pady=10)

remove_button = ttk.Button(frame, text="Remove Selected Duplicates", command=remove_duplicates)
remove_button.pack(pady=10)

remove_all_button = ttk.Button(frame, text="Remove All Duplicates", command=remove_all_duplicates)
remove_all_button.pack(pady=10)

file_list = tk.Listbox(frame, width=80, height=20)
file_list.pack()

status_label = ttk.Label(frame, text="")
status_label.pack(pady=10)

root.mainloop()

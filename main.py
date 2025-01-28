import os
import random
import tkinter as tk
from tkinter import messagebox, filedialog
from threading import Thread

def flip_random_bit(byte_value):
    bit_position = random.randint(0, 7)
    return byte_value ^ (1 << bit_position)

def set_bit_to_zero(byte_value):
    bit_position = random.randint(0, 7)
    mask = ~(1 << bit_position)
    return byte_value & mask

def corrupt_file(file_path, intensity, method):
    try:
        with open(file_path, 'rb') as file:
            content = bytearray(file.read())

        chance = intensity / 100
        for i in range(len(content)):
            if random.random() < chance:
                if method == "flip":
                    content[i] = flip_random_bit(content[i])
                elif method == "zero":
                    content[i] = set_bit_to_zero(content[i])

        with open(file_path, 'wb') as file:
            file.write(content)
        return f"Corrupted file: {file_path}"
    except Exception as e:
        return f"Error corrupting {file_path}: {e}"

processed_files = set()

def find_next_file(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if file_path not in processed_files:
                return file_path
    return None

def start_corruption(directory, intensity, method, status_label):
    global stop_corruption_flag, processed_files
    stop_corruption_flag = False

    while not stop_corruption_flag:
        file_to_corrupt = find_next_file(directory)
        if not file_to_corrupt:
            status_label.config(text="No more files found to corrupt.")
            break

        result = corrupt_file(file_to_corrupt, intensity, method)
        processed_files.add(file_to_corrupt)
        status_label.config(text=result)

    if stop_corruption_flag:
        status_label.config(text="Corruption stopped.")

def reset_corruption_status(status_label):
    global processed_files
    processed_files = set() #fix: after finishing or stopping the last task you couldnt start from beginning which was anoyying >:(
    status_label.config(text="Status: Waiting")

def create_gui():
    root = tk.Tk()
    root.title("PyCorrupter")

    tk.Label(root, text="Directory to Corrupt:").pack(pady=5)
    directory_label = tk.Label(root, text="", width=50, anchor="w", bg="white", relief="sunken")
    directory_label.pack(pady=5)

    def browse_directory():
        selected_directory = filedialog.askdirectory()
        if selected_directory:
            directory_label.config(text=selected_directory)

    browse_button = tk.Button(root, text="Browse", command=browse_directory)
    browse_button.pack(pady=5)

    tk.Label(root, text="Corruption Intensity (%):").pack(pady=5)
    intensity_entry = tk.Entry(root, width=10)
    intensity_entry.pack(pady=5)
    intensity_entry.insert(0, "30")

    tk.Label(root, text="Corruption Method:").pack(pady=5)
    method_var = tk.StringVar(value="flip")
    method_dropdown = tk.OptionMenu(root, method_var, "flip", "zero")
    method_dropdown.pack(pady=5)

    status_label = tk.Label(root, text="Status: Waiting", fg="blue")
    status_label.pack(pady=10)

    def on_start():
        directory = directory_label.cget("text")
        try:
            intensity = int(intensity_entry.get())
            if not os.path.exists(directory):
                messagebox.showerror("Error", "The specified directory does not exist.")
                return
            if intensity < 0 or intensity > 100:
                messagebox.showerror("Error", "Intensity must be between 0 and 100.")
                return
            method = method_var.get()
            status_label.config(text="Corrupting files...")
            Thread(target=start_corruption, args=(directory, intensity, method, status_label), daemon=True).start()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid intensity percentage.")

    start_button = tk.Button(root, text="Start Corruption", command=on_start)
    start_button.pack(pady=5)

    def on_stop():
        global stop_corruption_flag
        stop_corruption_flag = True

    stop_button = tk.Button(root, text="Stop Corruption", command=on_stop)
    stop_button.pack(pady=5)

    def on_reset():
        reset_corruption_status(status_label)

    reset_button = tk.Button(root, text="Reset", command=on_reset)
    reset_button.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    create_gui()

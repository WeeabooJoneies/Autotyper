import time
import threading
import tkinter as tk
import pyautogui
from pynput import keyboard

def start_spam(character, interval, repetitions):
    def spam_thread():
        for _ in range(repetitions) if repetitions is not None else iter(int, 1):
            if not spamming:
                break
            pyautogui.typewrite(character)
            time.sleep(interval)

    spam_thread = threading.Thread(target=spam_thread)
    spam_thread.start()

def stop_spam():
    global spamming
    spamming = False

def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def is_int(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

spamming = False
start_button = None
stop_button = None

def start_spam_from_ui():
    global spamming
    global start_button
    global stop_button
    if not spamming:
        character = char_entry.get()
        interval = interval_entry.get()
        repetitions = repetitions_entry.get()
        if not character:
            spam_label.config(text="Please enter a character to spam.")
            return
        if not is_float(interval):
            spam_label.config(text="Interval should be a number.")
            return
        if repetitions_var.get() == "Specific" and (not is_int(repetitions) or int(repetitions) <= 0):
            spam_label.config(text="Repetitions should be a positive integer.")
            return
        spam_label.config(text="")
        spamming = True
        start_spam(character, float(interval), int(repetitions) if repetitions_var.get() == "Specific" else None)
        start_button.config(state=tk.DISABLED)
        stop_button.config(state=tk.NORMAL)

def stop_spam_from_ui():
    global spamming
    global start_button
    global stop_button
    if spamming:
        spamming = False
        start_button.config(state=tk.NORMAL)
        stop_button.config(state=tk.DISABLED)
        spam_label.config(text="Spam stopped.")

def on_key_release(key):
    if key == keyboard.Key.f6:
        start_spam_from_ui()
    elif key == keyboard.Key.f5:
        stop_spam_from_ui()

def validate_input(P):
    if P == "" or P == ".":
        return True
    try:
        float(P)
        return True
    except ValueError:
        return False

root = tk.Tk()
root.title("Spam App")
root.geometry("800x400")  # Set the window size to 800x400

char_label = tk.Label(root, text="Enter a character:")
char_label.pack()

char_entry = tk.Entry(root)
char_entry.pack()

interval_label = tk.Label(root, text="Enter the interval (in seconds):")
interval_label.pack()

validate_interval_input = root.register(validate_input)
interval_entry = tk.Entry(root, validate="key", validatecommand=(validate_interval_input, '%P'))
interval_entry.pack()

repetitions_label = tk.Label(root, text="Repetitions:")
repetitions_label.pack()

repetitions_var = tk.StringVar(value="Infinite")

repetitions_radio_infinite = tk.Radiobutton(root, text="Infinite", variable=repetitions_var, value="Infinite")
repetitions_radio_infinite.pack()

repetitions_radio_specific = tk.Radiobutton(root, text="Specific", variable=repetitions_var, value="Specific")
repetitions_radio_specific.pack()

repetitions_entry = tk.Entry(root, validate="key", validatecommand=(validate_interval_input, '%P'))
repetitions_entry.pack()

spam_button = tk.Button(root, text="Start Spam (F6)", command=start_spam_from_ui)
spam_button.pack()

stop_button = tk.Button(root, text="Stop Spam (F5)", command=stop_spam_from_ui, state=tk.DISABLED)
stop_button.pack()

spam_label = tk.Label(root, text="", font=("Arial", 20))
spam_label.pack()

start_button = spam_button
stop_button = stop_button

listener = keyboard.Listener(on_release=on_key_release)
listener.start()

root.mainloop()

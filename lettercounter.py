import tkinter as tk
from tkinter import ttk
from pynput import keyboard
import time
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class LetterCounterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Global Letter Counter")
        self.root.geometry("1000x900")
        self.root.minsize(800, 600)

        # Apply a ttkbootstrap theme
        self.style = ttkb.Style("darkly")

        # Main frame
        self.main_frame = ttkb.Frame(root, padding="20 20 20 20")
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        # Configure grid
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=0)
        self.main_frame.grid_rowconfigure(1, weight=0)
        self.main_frame.grid_rowconfigure(2, weight=0)
        self.main_frame.grid_rowconfigure(3, weight=1)
        self.main_frame.grid_rowconfigure(4, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Counter labels
        self.top_counter_label = ttkb.Label(self.main_frame, text="Global Letter Count: 0", font=('Helvetica', 16, 'bold'))
        self.top_counter_label.grid(row=0, column=0, pady=10, sticky="ew")

        self.speed_label = ttkb.Label(self.main_frame, text="Typing Speed: 0 CPM", font=('Helvetica', 16, 'bold'))
        self.speed_label.grid(row=1, column=0, pady=10, sticky="ew")

        # Buttons for control
        self.button_frame = ttkb.Frame(self.main_frame)
        self.button_frame.grid(row=2, column=0, pady=20, sticky="ew")

        self.start_button = ttkb.Button(self.button_frame, text="Start Tracking", command=self.start_tracking, bootstyle=SUCCESS)
        self.start_button.pack(side=tk.LEFT, padx=20, pady=20)

        self.stop_button = ttkb.Button(self.button_frame, text="Stop Tracking", command=self.stop_tracking, bootstyle=WARNING)
        self.stop_button.pack(side=tk.LEFT, padx=20, pady=20)

        self.reset_button = ttkb.Button(self.button_frame, text="Reset Counters", command=self.reset_counters, bootstyle=DANGER)
        self.reset_button.pack(side=tk.LEFT, padx=20, pady=20)

        # Initialize counters
        self.letter_count = 0
        self.start_time = None
        self.tracking = False
        self.last_typing_time = None
        self.typing_duration = 0

        # Start the global key listener
        self.listener = keyboard.Listener(on_press=self.on_key_press)
        self.listener.start()

        # Graph setup
        self.letter_count_frame = ttkb.Frame(self.main_frame, padding="10 10 10 10")
        self.letter_count_frame.grid(row=3, column=0, pady=(0, 10), sticky="nsew")

        self.typing_speed_frame = ttkb.Frame(self.main_frame, padding="10 10 10 10")
        self.typing_speed_frame.grid(row=4, column=0, pady=(10, 0), sticky="nsew")

        self.fig1, self.ax1 = plt.subplots(figsize=(8, 4), facecolor='#1a1a1a')
        self.canvas1 = FigureCanvasTkAgg(self.fig1, master=self.letter_count_frame)
        self.canvas1.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.fig2, self.ax2 = plt.subplots(figsize=(8, 4), facecolor='#1a1a1a')
        self.canvas2 = FigureCanvasTkAgg(self.fig2, master=self.typing_speed_frame)
        self.canvas2.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.letter_count_history = []
        self.time_history = []
        self.speed_history = []

        self.root.bind('<Configure>', self.on_resize)

        # Timer for updating the UI periodically
        self.update_interval = 1000  # milliseconds
        self.update_ui()

    def on_key_press(self, key):
        if self.tracking:
            try:
                if key.char and key.char.isalpha():
                    current_time = time.time()
                    if self.last_typing_time:
                        # Accumulate typing duration only if the break is less than 10 seconds
                        if current_time - self.last_typing_time <= 10:
                            self.typing_duration += current_time - self.last_typing_time

                    self.last_typing_time = current_time
                    self.letter_count += 1
                    if self.start_time is None:
                        self.start_time = current_time
            except AttributeError:
                pass

    def update_labels(self):
        self.top_counter_label.config(text=f"Global Letter Count: {self.letter_count}")
        if self.start_time and self.typing_duration > 0:
            elapsed_time = time.time() - self.start_time
            cpm = (self.letter_count / self.typing_duration) * 60
            self.speed_label.config(text=f"Typing Speed: {int(cpm)} CPM")

    def update_graphs(self):
        self.ax1.clear()
        self.ax1.plot(self.time_history, self.letter_count_history, label='Letter Count', color='blue', linewidth=2)
        self.ax1.set_title('Letter Count Over Time', color='white')
        self.ax1.set_ylabel('Count', color='white')
        self.ax1.legend()
        self.ax1.grid(True)
        self.ax1.set_facecolor('#333')
        self.ax1.tick_params(axis='x', colors='white')
        self.ax1.tick_params(axis='y', colors='white')

        self.ax2.clear()
        self.ax2.plot(self.time_history, self.speed_history, label='Typing Speed (CPM)', color='red', linewidth=2)
        self.ax2.set_title('Typing Speed Over Time', color='white')
        self.ax2.set_ylabel('CPM', color='white')
        self.ax2.set_xlabel('Time (s)', color='white')
        self.ax2.legend()
        self.ax2.grid(True)
        self.ax2.set_facecolor('#333')
        self.ax2.tick_params(axis='x', colors='white')
        self.ax2.tick_params(axis='y', colors='white')

        self.canvas1.draw()
        self.canvas2.draw()

    def on_resize(self, event):
        # Ensure the graphs resize properly when the window is resized
        self.canvas1.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.canvas2.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def start_tracking(self):
        self.tracking = True
        if self.start_time is None:
            self.start_time = time.time()
        self.last_typing_time = time.time()
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

    def stop_tracking(self):
        self.tracking = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def reset_counters(self):
        self.letter_count = 0
        self.start_time = None
        self.last_typing_time = None
        self.typing_duration = 0
        self.letter_count_history.clear()
        self.time_history.clear()
        self.speed_history.clear()
        self.update_labels()
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.update_graphs()

    def update_ui(self):
        if self.tracking:
            if self.start_time and self.typing_duration > 0:
                elapsed_time = time.time() - self.start_time
                self.letter_count_history.append(self.letter_count)
                self.time_history.append(elapsed_time)
                cpm = (self.letter_count / self.typing_duration) * 60
                self.speed_history.append(cpm)
            self.update_labels()
            self.update_graphs()
        self.root.after(self.update_interval, self.update_ui)

    def on_close(self):
        self.listener.stop()
        self.root.destroy()

if __name__ == "__main__":
    root = ttkb.Window(themename="darkly")
    app = LetterCounterApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()

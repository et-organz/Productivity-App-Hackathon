import tkinter as tk
from tkinter import messagebox, simpledialog
import time

class PomodoroTimer:
    def __init__(self, master):
        self.master = master
        self.master.title("Pomodoro Timer")

        self.work_duration = 25 * 60  # Default 25 minutes in seconds
        self.short_break_duration = 5 * 60  # Default 5 minutes in seconds
        self.long_break_duration = 45 * 60  # Default 45 minutes in seconds
        self.cycle_count = 0
        self.is_running = False
        self.time_left = self.work_duration

        self.label = tk.Label(master, text="Pomodoro Timer", font=("Helvetica", 24))
        self.label.pack(pady=10)

        self.timer_label = tk.Label(master, text=self.format_time(self.time_left), font=("Helvetica", 48))
        self.timer_label.pack(pady=20)

        self.start_button = tk.Button(master, text="Start", command=self.start_timer, font=("Helvetica", 14))
        self.start_button.pack(side=tk.LEFT, padx=20)

        self.reset_button = tk.Button(master, text="Reset", command=self.reset_timer, font=("Helvetica", 14))
        self.reset_button.pack(side=tk.RIGHT, padx=20)

        self.settings_button = tk.Button(master, text="Settings", command=self.open_settings, font=("Helvetica", 14))
        self.settings_button.pack(pady=10)

    def format_time(self, seconds):
        minutes, seconds = divmod(seconds, 60)
        return f"{minutes:02}:{seconds:02}"

    def start_timer(self):
        if not self.is_running:
            self.is_running = True
            self.countdown()

    def countdown(self):
        if self.time_left > 0:
            self.timer_label.config(text=self.format_time(self.time_left))
            self.time_left -= 1
            self.master.after(1000, self.countdown)
        else:
            self.is_running = False
            self.cycle_count += 1
            if self.cycle_count % 4 == 0:  # Every 4 cycles, take a long break
                self.time_left = self.long_break_duration
                self.notify("Time for a long break!")
            else:
                self.time_left = self.short_break_duration if self.time_left == self.work_duration else self.work_duration
                self.notify("Time to focus!" if self.time_left == self.work_duration else "Time for a short break!")

            self.start_timer()  # Automatically start the next session

    def notify(self, message):
        messagebox.showinfo("Pomodoro Timer", message)

    def reset_timer(self):
        self.is_running = False
        self.cycle_count = 0
        self.time_left = self.work_duration
        self.timer_label.config(text=self.format_time(self.time_left))

    def open_settings(self):
        work_minutes = simpledialog.askinteger("Work Duration", "Enter work duration in minutes:", initialvalue=25)
        short_break_minutes = simpledialog.askinteger("Short Break Duration", "Enter short break duration in minutes:", initialvalue=5)
        long_break_minutes = simpledialog.askinteger("Long Break Duration", "Enter long break duration in minutes:", initialvalue=45)

        if work_minutes is not None:
            self.work_duration = work_minutes * 60
        if short_break_minutes is not None:
            self.short_break_duration = short_break_minutes * 60
        if long_break_minutes is not None:
            self.long_break_duration = long_break_minutes * 60

        self.reset_timer()  # Reset the timer to apply new settings

root = tk.Tk()
pomodoro_timer = PomodoroTimer(root)
root.mainloop()
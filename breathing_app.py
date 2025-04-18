import tkinter as tk
from tkinter import messagebox
import time

class BreathingApp:
    def __init__(self, master,minutes=300):
        self.master = master
        self.master.title("Breathing Exercise")

        self.label = tk.Label(master, text="Get Ready to Breathe", font=("Helvetica", 24))
        self.label.pack(pady=20)

        self.instruction_label = tk.Label(master, text="", font=("Helvetica", 18))
        self.instruction_label.pack(pady=20)

        self.timer_label = tk.Label(master, text="", font=("Helvetica", 48))
        self.timer_label.pack(pady=20)

        self.start_button = tk.Button(master, text="Start Breathing Exercise", command=self.start_breathing, font=("Helvetica", 14))
        self.start_button.pack(pady=10)


        self.breathing_cycle = [
            ("Breathe In", 4),  # Inhale for 4 seconds
            ("Hold", 4),        # Hold for 4 seconds
            ("Breathe Out", 6), # Exhale for 6 seconds
            ("Hold", 2)         # Hold for 2 seconds
        ]
        cycle_time = 0
        for name,time in self.breathing_cycle:
            cycle_time += time
        self.num_cycles = minutes//cycle_time

    def start_breathing(self):

        self.start_button.config(state=tk.DISABLED)  # Disable the button during the exercise
        self.breathing_sequence()

    def breathing_sequence(self):
        for cycle in range(self.num_cycles):
            for instruction, duration in self.breathing_cycle:
                self.instruction_label.config(text=instruction)
                self.timer_label.config(text=str(duration))  # Set timer label to duration
                self.master.update()  # Update the GUI

                # Countdown timer
                for remaining in range(duration, 0, -1):
                    self.timer_label.config(text=str(remaining))  # Update timer display
                    self.master.update()  # Update the GUI
                    time.sleep(1)  # Wait for 1 second

        self.instruction_label.config(text="Great job! Take a moment to relax.")
        self.timer_label.config(text="")  # Clear the timer display
        self.start_button.config(state=tk.NORMAL)  # Re-enable the button



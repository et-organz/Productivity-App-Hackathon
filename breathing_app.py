import tkinter as tk
from tkinter import messagebox
import time

class BreathingApp:
    def __init__(self, master):
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

        self.cycle_count_label = tk.Label(master, text="Number of Cycles:", font=("Helvetica", 14))
        self.cycle_count_label.pack(pady=10)

        self.cycle_count_entry = tk.Entry(master, font=("Helvetica", 14))
        self.cycle_count_entry.pack(pady=10)
        self.cycle_count_entry.insert(0, "3")  # Default to 3 cycles

        self.breathing_cycle = [
            ("Breathe In", 4),  # Inhale for 4 seconds
            ("Hold", 4),        # Hold for 4 seconds
            ("Breathe Out", 6), # Exhale for 6 seconds
            ("Hold", 2)         # Hold for 2 seconds
        ]

    def start_breathing(self):
        try:
            self.num_cycles = int(self.cycle_count_entry.get())
            if self.num_cycles <= 0:
                raise ValueError("Number of cycles must be positive.")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number of cycles.")
            return

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


root = tk.Tk()
app = BreathingApp(root)
root.mainloop()
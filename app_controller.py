import tkinter as tk
from tkinter import messagebox, simpledialog
import random

from website_blocker_app import WebsiteBlockerApp
from breathing_app import BreathingApp
from drawing_app import DrawingApp
from self_explanation_app import SelfExplanationApp
from integration_app import InterrogationApp
from practice_testing_app import PracticeTestingApp
import os
from dotenv import load_dotenv
import openai
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
class AppController:
    def __init__(self):
        self.root = tk.Tk()
        self.chat_gpt_messages = [] 


        self.root.withdraw()  # Hide the main window initially
        self.open_ai_session = openai
        self.apps = {
            "website_blocker": WebsiteBlockerApp,
            "breathing": BreathingApp,
            "drawing": DrawingApp,
            "pomodoro": PomodoroTimer,
            "explanation": SelfExplanationApp,
            "integration": InterrogationApp,
            "practice": PracticeTestingApp
        }

        self.app_instances = {}
        self.app_states = {name: False for name in self.apps}

    def confirmation_window(self):
        """Create a confirmation window to start the Pomodoro timer."""
        confirm_window = tk.Toplevel(self.root)
        confirm_window.title("Choose an option")

        yes_button = tk.Button(confirm_window, text="Begin Focusing", command=lambda: self.start_pomodoro(confirm_window), font=("Helvetica", 14))
        yes_button.pack(side=tk.LEFT, padx=20)

        no_button = tk.Button(confirm_window, text="Open Blocked Sites", command=lambda: self.open_app("website_blocker"), font=("Helvetica", 14))
        no_button.pack(side=tk.RIGHT, padx=20)

    def start_pomodoro(self, confirm_window):
        """Start the Pomodoro timer and close the confirmation window."""
        if "website_blocker" in  self.app_instances:
            self.app_instances["website_blocker"].block_websites()
        confirm_window.destroy()  # Close the confirmation window
        self.open_app("pomodoro")  # Open the Pomodoro timer

    def open_app(self, app_name):
        if app_name in self.apps and not self.app_states[app_name]:
            new_window = tk.Toplevel(self.root)
            if app_name == "pomodoro":
                self.app_instances[app_name] = self.apps[app_name](new_window)  # Create an instance of the app class
            else:
                self.app_instances[app_name] = self.apps[app_name](new_window,self.chat_gpt_messages)  # Create an instance of the app class

            self.app_states[app_name] = True

            def on_close():
                self.app_states[app_name] = False
                new_window.destroy()

            new_window.protocol("WM_DELETE_WINDOW", on_close)

    def close_app(self, app_name):
        if app_name in self.app_instances:
            self.chat_gpt_messages = self.app_instances[app_name].messages
            self.app_instances[app_name].master.destroy()
            self.app_states[app_name] = False

    def is_app_open(self, app_name):
        return self.app_states.get(app_name, False)

    def minimize_app(self, app_name):
        if app_name in self.app_instances:
            self.app_instances[app_name].root.iconify()

    def maximize_app(self, app_name):
        if app_name in self.app_instances:
            self.app_instances[app_name].root.deiconify()

    def get_random_app_name(self):
        choices = [name for name in ["breathing", "drawing", "explanation","integration"] if not self.app_states[name]]
        if choices:
            return random.choice(choices)
    def find_open_app(self):
        res = None
        res = [app_name for app_name, app_state in  self.app_states if app_state]
        return res


# TODO: IM NOT HAPPY WITH THIS BUT WERE DOING THIS TO AVOID CIRCULUAR IMPORTS
class PomodoroTimer(AppController):
    def __init__(self, master):
        super().__init__()  # Call the parent constructor
        self.master = master
        self.master.title("Pomodoro Timer")
        self.break_app = None
        self.work_duration = 25 * 60  # Default 25 minutes in seconds
        self.short_break_duration = 5 * 60  # Default 5 minutes in seconds
        self.long_break_duration = 15 * 60  # Default 15 minutes in seconds
        self.working = True
        self.cycle_count = 0
        self.is_running = False
        self.time_left = self.work_duration

        self.label = tk.Label(master, text="Pomodoro Timer", font=("Helvetica", 24))
        self.label.pack(pady=10)

        self.status_label = tk.Label(master, text="Status: Working", font=("Helvetica", 18))
        self.status_label.pack(pady=10)

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
            if self.working == False:
                self.working = True
                self.time_left = self.work_duration
                self.status_label.config(text="Status: Working")
                self.notify("Time to get back to work!\n closing " + self.break_app + " app")
                self.close_app(self.break_app)
                self.break_app = None
                self.start_timer()
                return
            self.cycle_count += 1
            if self.cycle_count % 4 == 0:  # Every 4 cycles, take a long break
                self.time_left = self.long_break_duration
                self.status_label.config(text="Status: Long Break")
                self.break_app = self.get_random_app_name()
                self.notify("Time for a long break! \n Opening "+ self.break_app + " app")
                self.open_app(self.break_app)  # Open a random app during long break
                self.working = False
            else:
                self.time_left = self.short_break_duration
                self.status_label.config(text="Status: Short Break")
                self.break_app = self.get_random_app_name()
                self.notify("Time for a short break!\n Opening "+ self.break_app + " app")
                self.open_app(self.break_app)  # Open a random app during short break
                self.working = False

            self.start_timer()  # Automatically start the next session

    def notify(self, message):
        messagebox.showinfo("Pomodoro Timer", message)

    def reset_timer(self):
        self.is_running = False
        self.working = True
        self.cycle_count = 0
        self.time_left = self.work_duration
        self.timer_label.config(text=self.format_time(self.time_left))
        self.status_label.config(text="Status: Working")  # Reset status label
        self.break_app = None
    def open_settings(self):
        work_minutes = simpledialog.askinteger("Work Duration", "Enter work duration in minutes:", initialvalue=25)
        short_break_minutes = simpledialog.askinteger("Short Break Duration", "Enter short break duration in minutes:", initialvalue=5)
        long_break_minutes = simpledialog.askinteger("Long Break Duration", "Enter long break duration in minutes:", initialvalue=15)

        if work_minutes is not None:
            self.work_duration = work_minutes * 60
        if short_break_minutes is not None:
            self.short_break_duration = short_break_minutes * 60
        if long_break_minutes is not None:
            self.long_break_duration = long_break_minutes * 60

        self.reset_timer()  # Reset the timer to apply new settings



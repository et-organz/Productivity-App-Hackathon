import tkinter as tk
import random

from website_blocker_app import WebsiteBlockerApp
from breathing_app import BreathingApp
from drawing_app import DrawingApp
from pomodoro_timer import PomodoroTimer
from mockups.encouragement_app import EncouragementApp

class AppController:
    def __init__(self, root):
        self.root = root
        self.root.title("Focus Toolkit")

        self.apps = {
            "website_blocker": WebsiteBlockerApp,
            "breathing": BreathingApp,
            "drawing": DrawingApp,
            "pomodoro": PomodoroTimer,
            "encouragement": EncouragementApp
        }

        self.app_instances = {}
        self.app_states = {name: False for name in self.apps}

    def open_app(self, app_name):
        if app_name in self.apps and not self.app_states[app_name]:
            new_window = tk.Toplevel(self.root)
            self.app_instances[app_name] = self.apps[app_name](new_window)
            self.app_states[app_name] = True

            def on_close():
                self.app_states[app_name] = False
                new_window.destroy()

            new_window.protocol("WM_DELETE_WINDOW", on_close)

    def close_app(self, app_name):
        if app_name in self.app_instances:
            self.app_instances[app_name].root.destroy()
            self.app_states[app_name] = False

    def is_app_open(self, app_name):
        return self.app_states.get(app_name, False)

    def minimize_app(self, app_name):
        if app_name in self.app_instances:
            self.app_instances[app_name].root.iconify()

    def maximize_app(self, app_name):
        if app_name in self.app_instances:
            self.app_instances[app_name].root.deiconify()

    def open_random_app(self):
        choices = [name for name in ["breathing", "drawing"] if not self.app_states[name]]
        if choices:
            self.open_app(random.choice(choices))
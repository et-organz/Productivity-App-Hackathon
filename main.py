# This is a sample Python script.
import openai
import os

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from app_controller import AppController
from web_tracking_app import create_web_tracking
import tkinter as tk
def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    create_web_tracking()
    app_controller = AppController()
    app_controller.confirmation_window()
    app_controller.root.mainloop()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/

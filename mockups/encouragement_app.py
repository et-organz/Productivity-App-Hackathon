import tkinter as tk
import threading
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class EncouragementApp:
    def __init__(self, root):
        self.root = root
        self.frame = tk.Frame(root)
        self.frame.pack()

        self.label = tk.Label(self.frame, text="Loading encouragement...", font=("Helvetica", 14))
        self.label.pack(pady=10)

        self.update_encouragement()

    def fetch_encouragement(self):
        prompt = "Give me a short encouraging message to stay focused during a work session."
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a motivational coach helping users stay focused."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            message = response.choices[0].message['content']
            return message
        except Exception as e:
            return f"Error: {e}"

    def update_encouragement(self):
        def fetch_and_update():
            message = self.fetch_encouragement()
            self.label.config(text=message)

        threading.Thread(target=fetch_and_update).start()
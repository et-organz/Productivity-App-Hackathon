import tkinter as tk
import threading
from dotenv import load_dotenv
from openai import OpenAI
import os
load_dotenv()


openai_session = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
class EncouragementApp:
    def __init__(self, root):
        self.master = root
        self.update_encouragement()

    def fetch_encouragement(self):
        prompt = "Give me a short encouraging message to stay focused during a work session."
        try:
            response = openai_session.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a motivational coach helping users stay focused. Your responses can not be longer than 10 words."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            message = response.choices[0].message.content
            return message
        except Exception as e:
            return f"Error: {e}"

    def update_encouragement(self):
        self.frame = tk.Frame(root)
        self.frame.pack()



        def fetch_and_update():
            message = self.fetch_encouragement()
            self.label = tk.Label(self.frame, text=message, font=("Helvetica", 14))
            self.label.pack(pady=10)
            self.master.after(3000, self.master.destroy)

        threading.Thread(target=fetch_and_update).start()

root = tk.Tk()
app = EncouragementApp(root)
root.mainloop()
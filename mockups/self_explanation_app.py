import tkinter as tk
import threading
from dotenv import load_dotenv
from openai import OpenAI
import os
load_dotenv()
class SelfExplanationApp:
    def __init__(self, root, openai_session):
        self.root = root
        self.openai_session = openai_session
        self.frame = tk.Frame(root)
        self.frame.pack(padx=10, pady=10)

        self.label = tk.Label(self.frame, text="What did you learn during this session?", font=("Helvetica", 12))
        self.label.pack(pady=5)

        self.learning_input = tk.Text(self.frame, height=5, width=50)
        self.learning_input.pack(pady=5)

        self.submit_button = tk.Button(self.frame, text="Submit", command=self.submit_learning)
        self.submit_button.pack(pady=5)

        self.response_label = tk.Label(self.frame, text="", wraplength=400, font=("Helvetica", 12))
        self.response_label.pack(pady=10)

        self.previous_learnings = []

    def submit_learning(self):
        current_learning = self.learning_input.get("1.0", tk.END).strip()
        if current_learning:
            self.previous_learnings.append(current_learning)
            self.generate_self_explanation(current_learning)

    def generate_self_explanation(self, current_learning):
        def task():
            prompt = (
                "You are a tutor helping a student reflect on what they learned. "
                f"The student just said: '{current_learning}'. "
                f"Their past learnings were: {self.previous_learnings[:-1]}. "
                "Help them explain how what they just learned relates to their past learnings."
            )

            try:
                response = self.openai_session.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You help students make connections between concepts they've learned."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7
                )
                message = response.choices[0].message['content']
                self.response_label.config(text=message)
            except Exception as e:
                self.response_label.config(text=f"Error: {e}")

        threading.Thread(target=task).start()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
root = tk.Tk()
app = SelfExplanationApp(root,client)
root.mainloop()
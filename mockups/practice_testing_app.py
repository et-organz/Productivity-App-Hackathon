import tkinter as tk
import threading
from dotenv import load_dotenv
from openai import OpenAI
import os
load_dotenv()
class PracticeTestingApp:
    def __init__(self, root, openai_session):
        self.root = root
        self.openai_session = openai_session
        self.frame = tk.Frame(root)
        self.frame.pack(padx=10, pady=10)

        self.label = tk.Label(self.frame, text="What is your learning goal?", font=("Helvetica", 12))
        self.label.pack(pady=5)

        self.goal_input = tk.Text(self.frame, height=3, width=50)
        self.goal_input.pack(pady=5)

        self.generate_button = tk.Button(self.frame, text="Generate Practice Test", command=self.generate_practice_test)
        self.generate_button.pack(pady=5)

        self.test_output_label = tk.Label(self.frame, text="", wraplength=400, font=("Helvetica", 12))
        self.test_output_label.pack(pady=10)

    def generate_practice_test(self):
        learning_goal = self.goal_input.get("1.0", tk.END).strip()
        if learning_goal:
            self.generate_test(learning_goal)

    def generate_test(self, learning_goal):
        def task():
            prompt = (
                f"Create a set of practice test questions based on the following learning goal: '{learning_goal}'. "
                "Provide multiple-choice questions and include answers after each question."
            )

            try:
                response = self.openai_session.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You help students generate practice test questions."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7
                )
                questions = response.choices[0].message['content']
                self.test_output_label.config(text=questions)
            except Exception as e:
                self.test_output_label.config(text=f"Error: {e}")

        threading.Thread(target=task).start()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
root = tk.Tk()
app = PracticeTestingApp(root,client)
root.mainloop()
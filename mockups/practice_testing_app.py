import tkinter as tk
import threading
from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()
openai_session = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
class PracticeTestingApp:
    def __init__(self, root):
        self.root = root
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

        # Track conversation messages
        self.messages = [
            {"role": "system", "content": "You help students generate practice test questions."}
        ]

    def generate_practice_test(self):
        learning_goal = self.goal_input.get("1.0", tk.END).strip()
        if learning_goal:
            self.generate_test(learning_goal)

    def generate_test(self, learning_goal):
        def task():
            user_message = (
                f"Create a set of practice test questions based on the following learning goal: '{learning_goal}'. "
                "Provide multiple-choice questions and include answers after each question."
            )

            # Add user message to conversation history
            self.messages.append({"role": "user", "content": user_message})

            try:
                response = openai_session.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=self.messages,
                    temperature=0.7
                )

                assistant_message = response.choices[0].message.content

                # Add assistant response to conversation history
                self.messages.append({"role": "assistant", "content": assistant_message})

                self.test_output_label.config(text=assistant_message)

            except Exception as e:
                self.test_output_label.config(text=f"Error: {e}")

        threading.Thread(target=task).start()

# Create OpenAI client and launch the app

root = tk.Tk()
app = PracticeTestingApp(root)
root.mainloop()

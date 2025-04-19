import tkinter as tk
import threading
from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

openai_session = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
class SelfExplanationApp:
    def __init__(self, root, messages):
        self.root = root
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

        # Track conversation messages
        self.messages = messages
        self.messages.append({"role": "system", "content": "You help students make connections between concepts they've learned."})

    def submit_learning(self):
        current_learning = self.learning_input.get("1.0", tk.END).strip()
        if current_learning:
            self.previous_learnings.append(current_learning)
            self.generate_self_explanation(current_learning)

    def generate_self_explanation(self, current_learning):
        def task():
            user_message = (
                "You are a tutor helping a student reflect on what they learned. "
                f"The student just said: '{current_learning}'. "
                f"Their past learnings were: {self.previous_learnings[:-1]}. "
                "Help them explain how what they just learned relates to their past learnings."
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

                self.response_label.config(text=assistant_message)

            except Exception as e:
                self.response_label.config(text=f"Error: {e}")





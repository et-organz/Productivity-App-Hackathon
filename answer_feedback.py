import os
import tkinter as tk
from tkinter import ttk
from dotenv import load_dotenv
import openai
import re

# Load environment variables
load_dotenv()

# Initialize OpenAI session
openai_session = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class AnswerFeedbackApp:
    def __init__(self, root, raw_user_input):
        self.root = root
        self.root.title("Answer Feedback")
        self.parsed_data = self.parse_user_input(raw_user_input)

        self.canvas = tk.Canvas(self.root)
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollable_frame = ttk.Frame(self.canvas)
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.scrollable_frame.bind("<Enter>", self._bind_mousewheel)
        self.scrollable_frame.bind("<Leave>", self._unbind_mousewheel)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.display_feedback()

    def _bind_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def parse_user_input(self, input_text):
        blocks = re.split(r"\n\s*\n", input_text.strip())
        parsed = {}
        current_url = None
        questions = []

        for block in blocks:
            lines = block.strip().split("\n")
            for line in lines:
                if line.startswith("From:"):
                    if current_url and questions:
                        parsed[current_url] = questions
                    current_url = line.replace("From:", "").strip()
                    questions = []
                elif line.startswith("Q:") and "A:" in line:
                    q, a = line.split("A:", 1)
                    questions.append((q.replace("Q:", "").strip(), a.strip()))
                elif line.startswith("Q:"):
                    question = line.replace("Q:", "").strip()
                    questions.append((question, ""))  # Empty answer
                elif line.startswith("A:") and questions:
                    answer = line.replace("A:", "").strip()
                    questions[-1] = (questions[-1][0], answer)  # Update last question with answer

        if current_url and questions:
            parsed[current_url] = questions

        return parsed

    def shorten_url(self, url, max_length=60):
        if len(url) <= max_length:
            return url
        return f"{url[:30]}...{url[-25:]}"  # Keeps beginning and end of the URL

    def display_feedback(self):
        for url, qas in self.parsed_data.items():
            short_url = self.shorten_url(url)
            url_label = ttk.Label(self.scrollable_frame, text=f"Feedback for: {short_url}", font=("Helvetica", 12, "bold"))
            url_label.pack(anchor="w", pady=(10, 5))

            for question, answer in qas:
                feedback = self.get_feedback_from_gpt(question, answer)

                ttk.Label(self.scrollable_frame, text=f"Q: {question}", font=("Helvetica", 11, "italic"), wraplength=500, justify="left").pack(anchor="w", padx=20, pady=(5, 0))
                ttk.Label(self.scrollable_frame, text=f"Your Answer: {answer}", font=("Helvetica", 11), wraplength=500, justify="left").pack(anchor="w", padx=20)
                ttk.Label(self.scrollable_frame, text=f"Feedback: {feedback}", font=("Helvetica", 11), wraplength=500, justify="left", foreground="green").pack(anchor="w", padx=20, pady=(0, 10))

        # Move Close button here, after all feedback has been rendered
        self.close_button = ttk.Button(self.scrollable_frame, text="Close", command=self.close_window)
        self.close_button.pack(pady=20)

    def get_feedback_from_gpt(self, question, answer):
        try:
            response = openai_session.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a teacher. Evaluate the student's answer to a question. If it's good, say 'Good job!'. If not, explain nicely what was missing or incorrect."
                    },
                    {
                        "role": "user",
                        "content": f"Question: {question}\nStudent Answer: {answer}"
                    }
                ],
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error getting feedback: {e}"

    def close_window(self):
        self.root.destroy()

def create_feedback(input):
    root = tk.Tk()
    app = AnswerFeedbackApp(root, input)
    root.mainloop()

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
                    questions.append((question, ""))
                elif line.startswith("A:") and questions:
                    answer = line.replace("A:", "").strip()
                    questions[-1] = (questions[-1][0], answer)

        if current_url and questions:
            parsed[current_url] = questions

        return parsed

    def display_feedback(self):
        for url, qas in self.parsed_data.items():
            url_label = ttk.Label(self.scrollable_frame, text=f"Feedback for: {url}", font=("Helvetica", 12, "bold"))
            url_label.pack(anchor="w", pady=(10, 5))

            for question, answer in qas:
                feedback = self.get_feedback_from_gpt(question, answer)

                ttk.Label(self.scrollable_frame, text=f"Q: {question}", font=("Helvetica", 11, "italic"), wraplength=500, justify="left").pack(anchor="w", padx=20, pady=(5, 0))
                ttk.Label(self.scrollable_frame, text=f"Your Answer: {answer}", font=("Helvetica", 11), wraplength=500, justify="left").pack(anchor="w", padx=20)
                ttk.Label(self.scrollable_frame, text=f"Feedback: {feedback}", font=("Helvetica", 11), wraplength=500, justify="left", foreground="green").pack(anchor="w", padx=20, pady=(0, 10))

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

if __name__ == "__main__":
    example_input = """
From: https://en.wikipedia.org/wiki/Comet
Q: 1. What are the main components of a comet and how do they contribute to the appearance of a comet as it approaches the Sun?
A: The main components of a commet are the nucleus, coma, tail, and hydrogen cloud. As the comet approaches the sun, the sun's heat causes the ice in the nucleus to sublimate creating the coman and forming the tail. The solar wind  from the sun pushes the ionized gases away from the sun forming the ion tail.

Q: 2. How do scientists classify comets based on their orbital characteristics and what are the differences between short-period and long-period comets?
A: Commets are classified based on their orbital period. Short-period commets have an orbital period of less than 200 years and are generally elliptical and low eccentricty. Long-period commets have an orbital period of more than 200 years and are hightly elongated or parabolic in shape.

Q: 3. Explain the process of sublimation in relation to comets and how it affects the development of the coma and tail during a comet's journey through the solar system.
A: Sublimation allows the nucleus of the commet to stay solid and cold while the suns sublimats the outer nucleus and creates the coma and tails. As the comet gets closer to the sun, it's sublimation increases causes the coma to expand and brighten, and when it moves away from the sun for both to fade.

From: https://en.wikipedia.org/wiki/Epic_poetry
Q: 1. What are the key characteristics of epic poetry as discussed in the article?
A: Key characteristics are a hero's legendary status, a vast setting, supernatural elements, elevated language and style, a great journey or quest, epic battles, and themess of honor, glory and fate.

Q: 2. How do epic poems differ from other forms of poetry, and what makes them unique?
A: Epic poems are user longer and tell a fully story. They usually center around a heroic figure. Epic poems are also usually use elevated, formal, and grand language. These poems also focus on purpose and are important cultural or religious artifacts for many cultures.

Q: 3. Can you identify and explain the significance of any specific examples of epic poetry mentioned in the article?
A: I'm not really sure. I haven't read many epic poems. I do like twinkle twinkle little star thought.
"""

    root = tk.Tk()
    app = AnswerFeedbackApp(root, example_input)
    root.mainloop()

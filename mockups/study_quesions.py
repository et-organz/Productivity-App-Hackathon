import os
import tkinter as tk
from tkinter import ttk
from dotenv import load_dotenv
import openai

# Load environment variables from .env file
load_dotenv()

# Create OpenAI session using new SDK style
openai_session = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class StudyQuestionApp:
    def __init__(self, root, urls):
        self.root = root
        self.urls = urls
        self.questions_by_url = {}
        self.answer_entries = {}

        self.root.title("Study Questions")
        self.create_widgets()
        self.fetch_questions()

    def create_widgets(self):
        # Canvas and scrollbar
        self.canvas = tk.Canvas(self.root)
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Scrollable frame inside the canvas
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas_frame = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Bind mouse wheel scrolling
        self.scrollable_frame.bind("<Enter>", self._bind_mousewheel)
        self.scrollable_frame.bind("<Leave>", self._unbind_mousewheel)

        # Pack canvas and scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def _bind_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def fetch_questions(self):
        for url in self.urls:
            questions = self.get_study_questions_from_url(url)
            self.questions_by_url[url] = questions
            self.display_questions(url, questions)

        # Place the submit button at the end of the scrollable content
        self.submit_button = ttk.Button(self.scrollable_frame, text="Submit Answers", command=self.submit_answers)
        self.submit_button.pack(pady=20)

    def get_study_questions_from_url(self, url):
        try:
            response = openai_session.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that creates study questions based on article content."
                    },
                    {
                        "role": "user",
                        "content": f"Generate 2-3 study questions based on this webpage: {url}"
                    }
                ],
                temperature=0.7
            )
            content = response.choices[0].message.content
            return content.strip().split("\n")
        except Exception as e:
            return [f"Failed to load questions for {url}: {e}"]

    def display_questions(self, url, questions):
        url_label = ttk.Label(self.scrollable_frame, text=url, font=("Helvetica", 12, "bold"))
        url_label.pack(anchor="w", pady=(10, 0))

        self.answer_entries[url] = []

        for q in questions:
            if not q.strip():
                continue
            q_label = ttk.Label(self.scrollable_frame, text=q.strip(), font=("Helvetica", 11), wraplength=500, justify="left")
            q_label.pack(anchor="w", padx=20)

            answer_entry = tk.Text(self.scrollable_frame, height=3, width=60, wrap="word")
            answer_entry.pack(padx=20, pady=5)
            self.answer_entries[url].append((q.strip(), answer_entry))

    def submit_answers(self):
        print("User Answers:\n" + "-" * 30)
        for url, entries in self.answer_entries.items():
            print(f"\nFrom: {url}")
            for question, entry_widget in entries:
                answer = entry_widget.get("1.0", "end").strip()
                print(f"Q: {question}")
                print(f"A: {answer}\n")

if __name__ == "__main__":
    # Test input
    example_links = [
        "https://en.wikipedia.org/wiki/Comet",
        "https://en.wikipedia.org/wiki/Epic_poetry"
    ]

    root = tk.Tk()
    app = StudyQuestionApp(root, example_links)
    root.mainloop()

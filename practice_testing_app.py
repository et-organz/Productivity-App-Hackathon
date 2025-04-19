import tkinter as tk
import threading
from dotenv import load_dotenv
from openai import OpenAI
import os
import re

load_dotenv()
openai_session = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class PracticeTestingApp:
    def __init__(self, root, messages):
        self.master = root
        self.messages = messages
        self.messages.append({
            "role": "system",
            "content": "You help students generate practice test questions."
        })

        self.frame = tk.Frame(root)
        self.frame.pack(padx=10, pady=10)

        self.label = tk.Label(self.frame, text="What did you learn this session? \nWhat do you want to be tested on?", font=("Helvetica", 12))
        self.label.pack(pady=5)

        self.goal_input = tk.Text(self.frame, height=3, width=50)
        self.goal_input.pack(pady=5)

        self.generate_button = tk.Button(self.frame, text="Generate Practice Test", command=self.generate_practice_test)
        self.generate_button.pack(pady=5)

        self.quiz_frame = tk.Frame(self.frame)
        self.quiz_frame.pack(pady=10)

    def generate_practice_test(self):
        learning_goal = self.goal_input.get("1.0", tk.END).strip()
        if learning_goal:
            self.goal_input.config(state="disabled")
            self.generate_button.config(state="disabled")
            self.generate_test(learning_goal)

    def generate_test(self, learning_goal):
        user_message = (
            f"You are a quiz generator. Based on the following learning goal: '{learning_goal}', "
            "generate exactly 4 multiple-choice questions. Each question should have 4 choices labeled A, B, C, and D. "
            "At the end of each question, write the correct answer clearly as 'Answer: X', where X is A, B, C, or D. "
            "Do not include explanations or extra text. Format exactly like this:\n\n"
            "1. Question text here\nA) Option A\nB) Option B\nC) Option C\nD) Option D\nAnswer: X\n\n"
            "Repeat this format for all 5 questions."
        )
        self.messages.append({"role": "user", "content": user_message})

        def task():
            try:
                response = openai_session.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=self.messages,
                    temperature=0.7
                )
                assistant_message = response.choices[0].message.content
                self.messages.append({"role": "assistant", "content": assistant_message})

                questions = self.parse_questions(assistant_message)
                self.render_questions(questions)

            except Exception as e:
                self.clear_quiz_frame()
                error_label = tk.Label(self.quiz_frame, text=f"Error: {e}", fg="red")
                error_label.pack()

        threading.Thread(target=task).start()

    def parse_questions(self, text):
        question_blocks = re.split(r"\n(?=\d+\.)", text.strip())
        parsed_questions = []

        for block in question_blocks:
            lines = block.strip().split("\n")
            if len(lines) < 6:
                continue
            question_text = lines[0]
            options = lines[1:5]
            answer_line = next((line for line in lines if "Answer:" in line), None)

            if answer_line:
                correct_letter = answer_line.split("Answer:")[-1].strip().upper()
                parsed_questions.append({
                    "question": question_text,
                    "options": options,
                    "answer": correct_letter
                })

        return parsed_questions

    def clear_quiz_frame(self):
        for widget in self.quiz_frame.winfo_children():
            widget.destroy()

    def render_questions(self, questions):
        self.clear_quiz_frame()
        for q in questions:
            q_frame = tk.Frame(self.quiz_frame)
            q_frame.pack(pady=10, anchor="w")

            question_label = tk.Label(q_frame, text=q["question"], font=("Helvetica", 12, "bold"), wraplength=500, justify="left")
            question_label.pack(anchor="w")

            result_label = tk.Label(q_frame, text="", font=("Helvetica", 11), wraplength=500, justify="left")
            result_label.pack(anchor="w", pady=(5, 0))

            btns = []
            for option in q["options"]:
                letter = option.strip()[0]

                btn = tk.Button(
                    q_frame,
                    text=option.strip(),
                    width=60,
                    anchor="w",
                    justify="left",
                    command=lambda l=letter, correct=q["answer"], label=result_label, b_list=btns: self.check_answer(
                        l, correct, label, b_list
                    )
                )
                btn.pack(anchor="w", pady=2)
                btns.append(btn)

    def check_answer(self, selected, correct, result_label, btns):
        for b in btns:
            b.config(state="disabled")

        if selected == correct:
            result_label.config(text="✅ Correct!", fg="green")
        else:
            result_label.config(text=f"❌ Incorrect. Correct answer: {correct}", fg="red")




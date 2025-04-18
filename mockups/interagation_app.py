import tkinter as tk
import threading
from app_controller import AppController  # Import the app_controller (assuming it handles OpenAI session)

class ElaborativeInterrogationApp:
    def __init__(self, root, openai_session):
        self.root = root
        self.openai_session = openai_session  # OpenAI session passed from the app controller
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

        self.previous_learnings = []  # Store past learnings

    def submit_learning(self):
        current_learning = self.learning_input.get("1.0", tk.END).strip()
        if current_learning:
            self.previous_learnings.append(current_learning)  # Add current learning to past learnings
            self.generate_elaborative_interrogation(current_learning)  # Generate questions based on new learning

    def generate_elaborative_interrogation(self, current_learning):
        """Generate elaborative interrogation questions using the LLM"""
        def task():
            prompt = (
                "You are a tutor helping a student explain what they learned. "
                f"The student just said: '{current_learning}'. "
                f"Their past learnings were: {self.previous_learnings[:-1]}. "
                "Ask the student questions that help them elaborate on the concept and explain how it connects to what they have learned before."
            )

            try:
                response = self.openai_session.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are a tutor helping students elaborate on their learning."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7
                )
                questions = response.choices[0].message['content']  # Get the generated questions from LLM
                self.response_label.config(text=questions)  # Display the questions in the UI
            except Exception as e:
                self.response_label.config(text=f"Error: {e}")

        threading.Thread(target=task).start()

if __name__ == "__main__":
    # Set up OpenAI session via app_controller (assuming it handles session management)
    app_controller = AppController()  # Initialize the app controller
    openai_session = app_controller.get_openai_session()  # Get the session

    root = tk.Tk()
    app = ElaborativeInterrogationApp(root, openai_session)
    root.mainloop()

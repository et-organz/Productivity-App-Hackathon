import tkinter as tk
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import logging
from dotenv import load_dotenv
import os
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ReadingTrackerApp:
    def __init__(self, root):
        self.root = root

        self.frame = tk.Frame(root)
        self.frame.pack(padx=10, pady=10)

        self.label = tk.Label(self.frame, text="Click to start tracking your reading", font=("Helvetica", 12))
        self.label.pack(pady=5)

        self.track_button = tk.Button(self.frame, text="Start Tracking", command=self.toggle_tracking)
        self.track_button.pack(pady=10)

        self.response_label = tk.Label(self.frame, text="", wraplength=400, font=("Helvetica", 12))
        self.response_label.pack(pady=10)

        self.driver = None
        self.is_tracking = False
        self.tracking_thread = None

    def toggle_tracking(self):
        if self.is_tracking:
            self.stop_tracking()
        else:
            self.start_tracking()

    def start_tracking(self):
        self.is_tracking = True
        self.track_button.config(text="Stop Tracking")
        self.response_label.config(text="Tracking started...")
        self.tracking_thread = threading.Thread(target=self.track_reading)
        self.tracking_thread.start()

    def track_reading(self):
        try:
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            self.driver = webdriver.Chrome(options=options)

            self.driver.get("https://en.wikipedia.org/wiki/Michel_de_Montaigne")
            time.sleep(2)

            reading_text = ""
            while self.is_tracking:
                body_content = self.driver.find_element(By.TAG_NAME, "body").text

                if body_content != reading_text:
                    reading_text = body_content
                    self.send_to_llm(reading_text)

                time.sleep(5)

            if self.driver:
                self.driver.quit()

        except Exception as e:
            logging.error(f"Error tracking reading: {e}")
            self.response_label.config(text=f"Error tracking: {e}")

    def send_to_llm(self, reading_text):
        def task():
            prompt = (
                "Based on the following text, generate a few test questions that can help the student review the information.\n\n"
                f"Text: {reading_text}\n\n"
                "Questions:"
            )
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a tutor helping students with their reading comprehension."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7
                )
                questions = response.choices[0].message.content
                self.response_label.config(text=questions)

            except Exception as e:
                self.response_label.config(text=f"Error: {e}")

        threading.Thread(target=task).start()

    def stop_tracking(self):
        self.is_tracking = False
        self.track_button.config(text="Start Tracking")
        self.response_label.config(text="Tracking stopped.")
        if self.driver:
            self.driver.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = ReadingTrackerApp(root)
    root.mainloop()

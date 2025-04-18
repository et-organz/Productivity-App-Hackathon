import tkinter as tk
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import openai
import logging


class ReadingTrackerApp:
    def __init__(self, root, openai_session):
        self.root = root
        self.openai_session = openai_session

        self.frame = tk.Frame(root)
        self.frame.pack(padx=10, pady=10)

        self.label = tk.Label(self.frame, text="Click to start tracking your reading", font=("Helvetica", 12))
        self.label.pack(pady=5)

        self.track_button = tk.Button(self.frame, text="Start Tracking", command=self.start_tracking)
        self.track_button.pack(pady=10)

        self.response_label = tk.Label(self.frame, text="", wraplength=400, font=("Helvetica", 12))
        self.response_label.pack(pady=10)

        self.driver = None
        self.is_tracking = False

    def start_tracking(self):
        """Starts tracking the webpage being read"""
        self.is_tracking = True
        self.track_button.config(state="disabled")  # Disable the button to prevent multiple clicks
        self.response_label.config(text="Tracking started...")
        threading.Thread(target=self.track_reading).start()  # Start the Selenium tracking in a separate thread

    def track_reading(self):
        """Tracks the text being read using Selenium"""
        try:
            # Set up the WebDriver (make sure you have the driver in your PATH)
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")  # Run Chrome in headless mode
            self.driver = webdriver.Chrome(options=options)

            # Open a webpage to read (example: Wikipedia)
            self.driver.get("https://en.wikipedia.org/wiki/OpenAI")  # You can change this URL
            time.sleep(2)  # Wait for the page to load

            # Continuously track the text content while reading
            reading_text = ""
            while self.is_tracking:
                # Get the body content of the page (you can target specific elements like paragraphs, etc.)
                body_content = self.driver.find_element(By.TAG_NAME, "body").text

                if body_content != reading_text:
                    reading_text = body_content
                    self.send_to_llm(reading_text)  # Send the updated content to LLM for testing

                time.sleep(5)  # Check every 5 seconds for updated content

            # Close the driver once tracking is stopped
            self.driver.quit()

        except Exception as e:
            logging.error(f"Error tracking reading: {e}")
            self.response_label.config(text=f"Error tracking: {e}")

    def send_to_llm(self, reading_text):
        """Sends the tracked content to the LLM for testing"""

        def task():
            prompt = (
                f"Based on the following text, generate a few test questions that can help the student review the information.\n\n"
                f"Text: {reading_text}\n\n"
                f"Questions: "
            )
            try:
                response = self.openai_session.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system",
                         "content": "You are a tutor helping students with their reading comprehension."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7
                )
                questions = response.choices[0].message['content']
                self.response_label.config(text=questions)  # Show the questions in the UI
            except Exception as e:
                self.response_label.config(text=f"Error: {e}")

        threading.Thread(target=task).start()

    def stop_tracking(self):
        """Stops tracking the reading"""
        self.is_tracking = False
        self.track_button.config(state="normal")  # Re-enable the button after tracking stops
        self.response_label.config(text="Tracking stopped.")


if __name__ == "__main__":
    # Set up OpenAI session (replace with your actual API key)
    openai.api_key = 'YOUR_OPENAI_API_KEY'

    root = tk.Tk()
    app = ReadingTrackerApp(root, openai)
    root.mainloop()

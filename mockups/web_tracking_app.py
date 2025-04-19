import os
import time
import sqlite3
import tkinter as tk
import threading
import shutil
from pathlib import Path
from datetime import datetime, timezone

class ReadingTrackerApp:
    def __init__(self, root):
        self.root = root
        self.is_tracking = False
        self.history_path = self.get_chrome_history_path()
        self.seen_urls = {}  # Dictionary to store URLs organized by date
        self.session_urls = set()  # Stores all URLs tracked during a session
        self.url_file_path = "seen_urls.txt"  # File to store URLs

        # Load URLs from the file if it exists
        self.load_seen_urls_from_file()

        self.frame = tk.Frame(root)
        self.frame.pack(padx=10, pady=10)

        self.label = tk.Label(self.frame, text="Click to start tracking websites using chrome browser", font=("Helvetica", 12))
        self.label.pack(pady=5)

        self.track_button = tk.Button(self.frame, text="Start Tracking", command=self.toggle_tracking)
        self.track_button.pack(pady=10)

        self.clear_button = tk.Button(self.frame, text="Clear Saved Sites", command=self.clear_saved_sites)
        self.clear_button.pack(pady=5)

        self.response_label = tk.Label(self.frame, text="", wraplength=400, font=("Helvetica", 12), justify="left")
        self.response_label.pack(pady=10)

    def get_chrome_history_path(self):
        home = str(Path.home())
        if os.name == "nt":
            return os.path.join(home, "AppData", "Local", "Google", "Chrome", "User Data", "Default", "History")
        elif os.name == "posix":
            return os.path.join(home, "Library", "Application Support", "Google", "Chrome", "Default", "History")
        else:
            raise Exception("Unsupported OS")

    def toggle_tracking(self):
        if self.is_tracking:
            self.is_tracking = False
            self.track_button.config(text="Start Tracking")
            self.display_tracked_websites()
        else:
            self.is_tracking = True
            self.session_urls.clear()  # Reset session URLs
            self.track_button.config(text="Stop Tracking")
            self.response_label.config(text="Tracking started...")
            threading.Thread(target=self.track_websites, daemon=True).start()

    def track_websites(self):
        while self.is_tracking:
            try:
                tmp_copy = "temp_chrome_history"
                shutil.copy2(self.history_path, tmp_copy)

                conn = sqlite3.connect(tmp_copy)
                cursor = conn.cursor()

                cursor.execute("SELECT url, title, last_visit_time FROM urls ORDER BY last_visit_time DESC LIMIT 10")
                results = cursor.fetchall()

                new_visits = []
                for url, title, last_visit_time in results:
                    visit_date = self.get_date_from_timestamp(last_visit_time)

                    if visit_date not in self.seen_urls:
                        self.seen_urls[visit_date] = set()

                    if url not in self.seen_urls[visit_date]:
                        self.seen_urls[visit_date].add(url)
                        display_url = self.shorten_url(url)
                        entry = f"{title}\n{display_url} ({visit_date})"
                        self.session_urls.add(entry)
                        new_visits.append(entry)
                        self.save_seen_urls_to_file()

                if new_visits:
                    self.response_label.config(text="\n\n".join(list(new_visits)[:5]))

                conn.close()
                os.remove(tmp_copy)
                time.sleep(5)

            except Exception as e:
                self.response_label.config(text=f"Error: {e}")
                time.sleep(10)

    def display_tracked_websites(self):
        if self.session_urls:
            self.response_label.config(
                text="Websites Tracked:\n\n" + "\n\n".join(sorted(self.session_urls))
            )
        else:
            self.response_label.config(text="No websites were tracked this session.")

    def save_seen_urls_to_file(self):
        with open(self.url_file_path, "w") as file:
            for date, urls in sorted(self.seen_urls.items()):
                file.write(f"{date}:\n")
                for url in sorted(urls):
                    file.write(f"  {url}\n")

    def load_seen_urls_from_file(self):
        if os.path.exists(self.url_file_path):
            with open(self.url_file_path, "r") as file:
                current_date = None
                for line in file:
                    line = line.strip()
                    if line.endswith(":"):
                        current_date = line[:-1]
                        self.seen_urls[current_date] = set()
                    elif current_date:
                        self.seen_urls[current_date].add(line)

    def clear_saved_sites(self):
        self.seen_urls.clear()
        if os.path.exists(self.url_file_path):
            with open(self.url_file_path, "w") as file:
                file.write("")
        self.response_label.config(text="All saved sites have been cleared.")

    def get_date_from_timestamp(self, timestamp):
        timestamp = timestamp / 1000000 - 11644473600
        visit_time = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        return visit_time.strftime('%Y-%m-%d')

    def shorten_url(self, url, length=15):
        return url if len(url) <= length else url[:length] + "..."

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Website Tracker")
    app = ReadingTrackerApp(root)
    root.mainloop()

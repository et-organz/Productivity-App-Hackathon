import tkinter as tk
from tkinter import messagebox
import vlc
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class AudioPlayer:
    def __init__(self, master):
        self.master = master
        self.master.title("YouTube Audio Player")

        # URL of the YouTube video (replace with your desired lo-fi beats video)
        self.youtube_url = "https://www.youtube.com/watch?v=jfKfPfyJRdk"  # Example URL

        # Create a VLC media player instance
        self.player = vlc.MediaPlayer(self.youtube_url)

        # Play button
        self.play_button = tk.Button(master, text="Play", command=self.play_audio, font=("Helvetica", 14))
        self.play_button.pack(pady=10)

        # Stop button
        self.stop_button = tk.Button(master, text="Stop", command=self.stop_audio, font=("Helvetica", 14))
        self.stop_button.pack(pady=10)

        # Volume slider
        self.volume_slider = tk.Scale(master, from_=0, to=100, orient=tk.HORIZONTAL, label="Volume", command=self.set_volume)
        self.volume_slider.set(50)  # Set default volume to 50%
        self.volume_slider.pack(pady=10)

    def play_audio(self):
        """Play the audio."""
        if self.player.play() == -1:
            messagebox.showerror("Error", "Could not play the audio. Please check the URL or your VLC installation.")

    def stop_audio(self):
        """Stop the audio."""
        self.player.stop()

    def set_volume(self, volume):
        """Set the volume of the audio player."""
        self.player.audio_set_volume(int(volume))


root = tk.Tk()
app = AudioPlayer(root)
root.mainloop()
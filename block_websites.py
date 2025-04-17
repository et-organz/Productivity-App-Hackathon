import os
import sys
import tkinter as tk
from tkinter import simpledialog, messagebox

# Path to the hosts file
if sys.platform == "win32":
    hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
else:
    hosts_path = "/etc/hosts"  # This is the path for macOS and Linux

# Redirect to localhost
redirect = "127.0.0.1"

class WebsiteBlockerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Website Blocker")

        self.blocked_websites = self.load_blocked_websites()

        self.label = tk.Label(master, text="Blocked Websites:", font=("Helvetica", 14))
        self.label.pack(pady=10)

        self.listbox = tk.Listbox(master, width=50, height=10)
        self.listbox.pack(pady=10)
        self.update_listbox()

        self.add_button = tk.Button(master, text="Add Website", command=self.add_website, font=("Helvetica", 12))
        self.add_button.pack(side=tk.LEFT, padx=20)

        self.remove_button = tk.Button(master, text="Remove Website", command=self.remove_website, font=("Helvetica", 12))
        self.remove_button.pack(side=tk.RIGHT, padx=20)

    def load_blocked_websites(self):
        """Load blocked websites from the hosts file."""
        blocked_websites = []
        try:
            with open(hosts_path, 'r') as file:
                for line in file:
                    if line.startswith(redirect):
                        blocked_websites.append(line.split()[1])
        except Exception as e:
            messagebox.showerror("Error", f"Could not read hosts file: {e}")
        return blocked_websites

    def update_listbox(self):
        """Update the listbox with the current blocked websites."""
        self.listbox.delete(0, tk.END)  # Clear the listbox
        for website in self.blocked_websites:
            self.listbox.insert(tk.END, website)

    def add_website(self):
        """Prompt the user to add a website to the block list."""
        website = simpledialog.askstring("Add Website", "Enter the website to block:")
        if website:
            self.blocked_websites.append(website.strip())
            self.block_websites()
            self.update_listbox()

    def remove_website(self):
        """Remove the selected website from the block list."""
        selected = self.listbox.curselection()
        if selected:
            website = self.blocked_websites[selected[0]]
            self.blocked_websites.remove(website)
            self.unblock_websites([website])
            self.update_listbox()
        else:
            messagebox.showwarning("Remove Website", "Please select a website to remove.")

    def block_websites(self):
        """Block the specified websites by modifying the hosts file."""
        with open(hosts_path, 'r+') as file:
            content = file.read()
            for website in self.blocked_websites:
                if website not in content:
                    file.write(f"{redirect} {website}\n")

    def unblock_websites(self, websites):
        """Unblock the specified websites by modifying the hosts file."""
        with open(hosts_path, 'r+') as file:
            lines = file.readlines()
            file.seek(0)
            for line in lines:
                if not any(website in line for website in websites):
                    file.write(line)
            file.truncate()  # Remove remaining lines


root = tk.Tk()
app = WebsiteBlockerApp(root)
root.mainloop()
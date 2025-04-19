import tkinter as tk
from tkinter import ttk
from pathlib import Path

class LinkSelectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Select Links")
        self.link_vars = []

        self.create_widgets()
        self.load_links()

    def create_widgets(self):
        self.frame = ttk.Frame(self.root, padding=10)
        self.frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(self.frame)
        self.scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.submit_button = ttk.Button(self.root, text="Submit", command=self.submit_selection)
        self.submit_button.pack(pady=10)

    def load_links(self):
        filepath = Path("seen_urls.txt")
        if not filepath.exists():
            label = ttk.Label(self.scrollable_frame, text="No seen_urls.txt found.", font=("Helvetica", 12))
            label.pack(pady=10)
            return

        current_date = None
        with filepath.open("r") as file:
            for line in file:
                line = line.strip()
                if line.endswith(":"):
                    current_date = line[:-1]
                    date_label = ttk.Label(self.scrollable_frame, text=current_date, font=("Helvetica", 14, "bold"))
                    date_label.pack(anchor="w", pady=(10, 0))
                elif line and current_date:
                    var = tk.BooleanVar()
                    chk = ttk.Checkbutton(self.scrollable_frame, text=line, variable=var)
                    chk.pack(anchor="w", padx=10)
                    self.link_vars.append((var, line))

    def submit_selection(self):
        selected_links = [url for var, url in self.link_vars if var.get()]
        if selected_links:
            print("Selected links:")
            for link in selected_links:
                print(link)
        else:
            print("No links selected.")

if __name__ == "__main__":
    root = tk.Tk()
    app = LinkSelectorApp(root)
    root.mainloop()

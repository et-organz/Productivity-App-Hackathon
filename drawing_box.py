import tkinter as tk

from tkinter import colorchooser




class DrawingApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Etch A Sketch")

        # Create a canvas for drawing
        self.canvas = tk.Canvas(master, bg="white", width=800, height=600)
        self.canvas.pack()

        # Initialize drawing state
        self.cursor_x, self.cursor_y = 400, 300  # Start in the center of the canvas
        self.last_x, self.last_y = self.cursor_x, self.cursor_y  # Last position for drawing
        self.constant_draw_mode = False
        self.current_color = "black"  # Default drawing color

        # Draw initial cursor
        self.cursor = self.canvas.create_oval(self.cursor_x - 5, self.cursor_y - 5, self.cursor_x + 5,
                                              self.cursor_y + 5, fill="red")

        # Bind mouse movement to update cursor position
        self.canvas.bind("<Motion>", self.update_cursor)

        # Bind keyboard events
        self.master.bind("<KeyPress>", self.key_press)

        # Instructions label
        self.instructions = tk.Label(master, text="Controls:\nArrow Keys: Move Cursor\nSpace: Toggle Draw Mode",
                                     font=("Helvetica", 12))
        self.instructions.pack(pady=10)

        # Color selection button
        self.color_button = tk.Button(master, text="Choose Color", command=self.change_color, font=("Helvetica", 14))
        self.color_button.pack(pady=10)

    def update_cursor(self, event):
        """Update the cursor position based on mouse movement."""
        self.cursor_x, self.cursor_y = event.x, event.y
        self.canvas.coords(self.cursor, self.cursor_x - 5, self.cursor_y - 5, self.cursor_x + 5, self.cursor_y + 5)

    def key_press(self, event):
        """Handle key presses for drawing with arrow keys and toggling draw mode."""
        if event.keysym == "space":
            self.constant_draw_mode = not self.constant_draw_mode  # Toggle draw mode
            if self.constant_draw_mode:
                self.instructions.config(text="Constant Draw Mode: Use Arrow Keys to Move and Draw")
            else:
                self.instructions.config(text="Controls:\nArrow Keys: Move Cursor\nSpace: Toggle Draw Mode")
        elif self.constant_draw_mode:
            if event.keysym == "Up":
                self.move_cursor(0, -10)
            elif event.keysym == "Down":
                self.move_cursor(0, 10)
            elif event.keysym == "Left":
                self.move_cursor(-10, 0)
            elif event.keysym == "Right":
                self.move_cursor(10, 0)

    def move_cursor(self, dx, dy):
        """Move the cursor and update its position."""
        # Update the last position before moving
        self.last_x, self.last_y = self.cursor_x, self.cursor_y

        # Update the cursor position
        self.cursor_x += dx
        self.cursor_y += dy

        # Update the cursor on the canvas
        self.canvas.coords(self.cursor, self.cursor_x - 5, self.cursor_y - 5, self.cursor_x + 5, self.cursor_y + 5)

        # Draw a line from the last position to the current position
        if self.constant_draw_mode:
            self.canvas.create_line(self.last_x, self.last_y, self.cursor_x, self.cursor_y, fill=self.current_color,
                                    width=2)

    def change_color(self):
        """Open a color chooser dialog to select a new drawing color."""
        color = colorchooser.askcolor(title="Choose Drawing Color")
        if color[1]:  # If a color was selected
            self.current_color = color[1]  # Set the current color to the selected color


root = tk.Tk()
app = DrawingApp(root)
root.mainloop()
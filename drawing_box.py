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
        self.key_draw_mode = False
        self.mouse_drawing = False
        self.current_color = "black"  # Default drawing color

        # Draw initial cursor
        self.cursor = self.canvas.create_oval(self.cursor_x - 5, self.cursor_y - 5, self.cursor_x + 5,
                                              self.cursor_y + 5, fill="red")

        # Bind mouse movement to update cursor position
        self.canvas.bind("<Motion>", self.update_cursor)

        # Bind keyboard events
        self.master.bind("<KeyPress>", self.key_press)



        # Bind mouse events to the canvas
        self.canvas.bind("<Button-1>", self.start_mouse_draw)  # Left mouse button
        self.canvas.bind("<B1-Motion>",  self.update_cursor)         # Mouse movement while button is pressed
        self.canvas.bind("<ButtonRelease-1>", self.stop_mouse_draw)  # Release the button

        self.instructions = tk.Label(master, text=f'Mouse Draw:\n Enter to switch to constant mouse draw mode \n Constant Mouse Draw : {self.mouse_drawing} \n Press space to switch to keyboard controls.',
                                     font=("Helvetica", 12))
        self.instructions.pack(pady=10)

        # Color selection button
        self.color_button = tk.Button(master, text="Choose Color", command=self.change_color, font=("Helvetica", 14))
        self.color_button.pack(pady=10)
        # Clear button
        self.clear_button = tk.Button(master, text="Clear", command=self.clear_canvas, font=("Helvetica", 14))
        self.clear_button.pack(pady=10)

    def get_mouse_instructions(self):
        """get string for mouse instructions"""
        text = f'Mouse Draw:\n Enter to switch to constant mouse draw mode \n Constant Mouse Draw : {self.mouse_drawing} \n Press space to switch to keyboard controls.'
        return str(text)

    def get_keyboard_instructions(self):
        """get string for keyboard instructions"""
        text = "Key Draw: Use Arrow Keys to Move and Draw \n Press space to switch to keyboard controls."
        return str(text)
    def start_mouse_draw(self, event):
        """Start drawing when the mouse button is pressed."""
        self.mouse_drawing = True
        self.last_x, self.last_y = self.cursor_x, self.cursor_y
    def mouse_draw(self, event):
        """Draw on the canvas while the mouse is moving."""
        if self.mouse_drawing:
            # Draw a line from the last position to the current position
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y, fill=self.current_color, width=2)
            self.last_x, self.last_y = event.x, event.y  # Update last position

    def stop_mouse_draw(self, event):
        """Stop drawing when the mouse button is released."""
        self.mouse_drawing = False
    def update_cursor(self, event):
        """Update the cursor position based on mouse movement."""
        if not self.key_draw_mode:
            self.cursor_x, self.cursor_y = event.x, event.y
            self.canvas.coords(self.cursor, self.cursor_x - 5, self.cursor_y - 5, self.cursor_x + 5, self.cursor_y + 5)
            self.mouse_draw(event)

    def clear_canvas(self):
        """Clear the drawing canvas."""
        self.canvas.delete("all")  # Delete all items on the canvas
        # Reset the cursor position
        self.cursor_x, self.cursor_y = 400, 300  # Reset to center of the canvas
        self.last_x, self.last_y = self.cursor_x, self.cursor_y
        # Redraw the cursor
        self.cursor = self.canvas.create_oval(self.cursor_x - 5, self.cursor_y - 5, self.cursor_x + 5,
                                              self.cursor_y + 5, fill="red")

    def key_press(self, event):
        """Handle key presses for drawing with arrow keys and toggling draw mode."""
        if event.keysym == 'Return':
            if self.mouse_drawing:
                self.stop_mouse_draw(None)
                self.instructions.config(
                    text=self.get_mouse_instructions())
            elif not self.mouse_drawing:
                self.start_mouse_draw(None)
                self.instructions.config(
                    text=self.get_mouse_instructions())

        if event.keysym == "space":
            self.key_draw_mode = not self.key_draw_mode  # Toggle draw mode
            if self.key_draw_mode:
                self.instructions.config(text=self.get_keyboard_instructions())
            else:
                self.instructions.config(
                    text=self.get_mouse_instructions())
        elif self.key_draw_mode:
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
        if self.key_draw_mode:
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
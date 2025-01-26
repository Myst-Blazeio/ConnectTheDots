import tkinter as tk
from tkinter import messagebox

class ConnectTheDots:
    def __init__(self, root):
        self.root = root
        self.root.title("Connect the Dots")

        # Game variables
        self.board_size = 4  # 4x4 grid of dots
        self.dot_radius = 10
        self.selection_radius = 15  # Radius for green circle selection highlight
        self.margin = 50
        self.line_width = 2
        self.cell_size = 100
        self.turn = 1  # 1 for Player 1, 2 for Player 2
        self.lines = set()
        self.squares = {}
        self.player_scores = {1: 0, 2: 0}
        self.selected_dot = None  # Initialize selected dot
        self.selection_circle = None  # For highlighting selected dot

        # Canvas for drawing
        canvas_width = self.margin * 2 + self.cell_size * (self.board_size - 1)
        canvas_height = canvas_width
        self.canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="white")
        self.canvas.pack()

        # Draw dots
        self.dots = {}
        for row in range(self.board_size):
            for col in range(self.board_size):
                x = self.margin + col * self.cell_size
                y = self.margin + row * self.cell_size
                dot_id = self.canvas.create_oval(x - self.dot_radius, y - self.dot_radius,
                                                 x + self.dot_radius, y + self.dot_radius,
                                                 fill="black", outline="")
                self.dots[(row, col)] = (x, y)

        # Bind mouse click
        self.canvas.bind("<Button-1>", self.handle_click)

        # Add score display
        self.score_label = tk.Label(root, text=self.get_score_text(), font=("Arial", 14))
        self.score_label.pack()

    def handle_click(self, event):
        # Get the closest dot to the click
        closest_dot = None
        min_distance = float("inf")
        for (row, col), (x, y) in self.dots.items():
            distance = ((event.x - x) ** 2 + (event.y - y) ** 2) ** 0.5
            if distance < min_distance:
                min_distance = distance
                closest_dot = (row, col)

        # If click was close enough to a dot, handle the logic
        if min_distance <= self.dot_radius * 2:
            self.select_dot(closest_dot)

    def select_dot(self, dot):
        # Store selected dot and connect to another
        if self.selected_dot is None:
            self.selected_dot = dot
            self.highlight_selection(dot)
        else:
            if self.is_valid_connection(self.selected_dot, dot):
                self.draw_line(self.selected_dot, dot)
                if not self.check_and_continue():  # Check if squares are formed and allow continuation
                    self.switch_turn()
                self.selected_dot = None
                self.clear_selection_highlight()
            else:
                messagebox.showinfo("Invalid Move", "Dots must be adjacent!")
                self.selected_dot = None
                self.clear_selection_highlight()

    def highlight_selection(self, dot):
        # Highlight the selected dot with a green circle
        x, y = self.dots[dot]
        self.selection_circle = self.canvas.create_oval(x - self.selection_radius, y - self.selection_radius,
                                                        x + self.selection_radius, y + self.selection_radius,
                                                        outline="green", width=2)

    def clear_selection_highlight(self):
        # Remove the green circle highlight
        if self.selection_circle:
            self.canvas.delete(self.selection_circle)
            self.selection_circle = None

    def is_valid_connection(self, dot1, dot2):
        # Check if two dots are adjacent
        (r1, c1), (r2, c2) = dot1, dot2
        return (abs(r1 - r2) == 1 and c1 == c2) or (abs(c1 - c2) == 1 and r1 == r2)

    def draw_line(self, dot1, dot2):
        # Draw a line between two dots
        if (dot1, dot2) not in self.lines and (dot2, dot1) not in self.lines:
            x1, y1 = self.dots[dot1]
            x2, y2 = self.dots[dot2]
            color = "red" if self.turn == 1 else "blue"
            self.canvas.create_line(x1, y1, x2, y2, fill=color, width=self.line_width)
            self.lines.add((dot1, dot2))

    def check_and_continue(self):
        # Check if a square is formed and fill it
        new_squares = 0
        for r in range(self.board_size - 1):
            for c in range(self.board_size - 1):
                square = [(r, c), (r, c + 1), (r + 1, c), (r + 1, c + 1)]
                if all(((square[i], square[j]) in self.lines or (square[j], square[i]) in self.lines)
                       for i, j in [(0, 1), (1, 3), (3, 2), (2, 0)]):
                    if tuple(square) not in self.squares:
                        color = "red" if self.turn == 1 else "blue"
                        x1, y1 = self.dots[square[0]]
                        x2, y2 = self.dots[square[3]]

                        # Animate square fill
                        self.animate_square_fill(x1, y1, x2, y2, color)

                        self.squares[tuple(square)] = self.turn
                        self.player_scores[self.turn] += 1
                        new_squares += 1

        self.update_score_display()  # Update score display
        if len(self.squares) == 9:  # Check if 9 squares are formed (end of the game)
            self.end_game()  # Call end_game when 9 squares are formed
        return new_squares > 0  # Return True if squares were formed

    def animate_square_fill(self, x1, y1, x2, y2, color):
        # Smoothly fill the square with a color
        steps = 10
        for i in range(steps):
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="",
                                         stipple="gray50" if i < steps - 1 else "")
            self.canvas.update()
            self.canvas.after(50)

    def switch_turn(self):
        # Switch turn if no new square is formed
        self.turn = 3 - self.turn

    def update_score_display(self):
        # Update the score display label
        self.score_label.config(text=self.get_score_text())

    def get_score_text(self):
        return f"Player 1 (Red): {self.player_scores[1]} | Player 2 (Blue): {self.player_scores[2]}"

    def end_game(self):
        # Check if the game has ended
        winner = max(self.player_scores, key=self.player_scores.get)
        messagebox.showinfo("Game Over", f"Player {winner} wins!")  # Show first message box
        # messagebox.showinfo("Congratulations!", f"Player {winner} is the winner!")  # Show second message box
        self.root.quit()  # Close the game window after both messages

# Run the game
if __name__ == "__main__":
    root = tk.Tk()
    game = ConnectTheDots(root)
    root.mainloop()

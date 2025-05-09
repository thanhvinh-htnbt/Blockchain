import tkinter as tk
from PIL import Image, ImageTk
import random

ROWS = 9
COLS = 12
MINES = 20
IMAGE_SIZE = 32  # bạn có thể điều chỉnh lại

class Cell:
    def __init__(self, x, y, label):
        self.x = x
        self.y = y
        self.label = label
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.neighbor_mines = 0

class Minesweeper:
    def __init__(self, master):
        self.master = master
        self.board = []

        # Load images
        self.blank_image = ImageTk.PhotoImage(Image.open("img_blank.png").resize((IMAGE_SIZE, IMAGE_SIZE)))
        self.flag_image = ImageTk.PhotoImage(Image.open("img_flag.png").resize((IMAGE_SIZE, IMAGE_SIZE)))
        self.mine_image = ImageTk.PhotoImage(Image.open("img_mine.png").resize((IMAGE_SIZE, IMAGE_SIZE)))
        self.number_images = {}
        for i in range(1, 8):
            img = Image.open(f"img_{i}.png").resize((IMAGE_SIZE, IMAGE_SIZE))
            self.number_images[i] = ImageTk.PhotoImage(img)

        self.setup()

    def setup(self):
        for x in range(ROWS):
            row = []
            for y in range(COLS):
                label = tk.Label(self.master, image=self.blank_image, width=IMAGE_SIZE, height=IMAGE_SIZE)
                label.image = self.blank_image
                label.grid(row=x, column=y)

                cell = Cell(x, y, label)
                label.bind("<Button-1>", lambda e, c=cell: self.reveal(c))
                label.bind("<Button-3>", lambda e, c=cell: self.flag(c))
                row.append(cell)
            self.board.append(row)

        self.place_mines()
        self.calculate_neighbors()

    def place_mines(self):
        count = 0
        while count < MINES:
            x = random.randint(0, ROWS - 1)
            y = random.randint(0, COLS - 1)
            cell = self.board[x][y]
            if not cell.is_mine:
                cell.is_mine = True
                count += 1

    def calculate_neighbors(self):
        for x in range(ROWS):
            for y in range(COLS):
                cell = self.board[x][y]
                if cell.is_mine:
                    continue
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < ROWS and 0 <= ny < COLS:
                            if self.board[nx][ny].is_mine:
                                cell.neighbor_mines += 1

    def reveal(self, cell):
        if cell.is_flagged or cell.is_revealed:
            return
        cell.is_revealed = True

        if cell.is_mine:
            cell.label.config(image=self.mine_image, bg="red")
            cell.label.image = self.mine_image
            self.game_over(False)
        else:
            if cell.neighbor_mines > 0:
                img = self.number_images[cell.neighbor_mines]
                cell.label.config(image=img)
                cell.label.image = img
            else:
                cell.label.config(image="", bg="lightgrey")

            if cell.neighbor_mines == 0:
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        nx, ny = cell.x + dx, cell.y + dy
                        if 0 <= nx < ROWS and 0 <= ny < COLS:
                            neighbor = self.board[nx][ny]
                            if not neighbor.is_revealed:
                                self.reveal(neighbor)
        self.check_win()

    def flag(self, cell):
        if cell.is_revealed:
            return
        cell.is_flagged = not cell.is_flagged
        if cell.is_flagged:
            cell.label.config(image=self.flag_image, text="", compound='center')
            cell.label.image = self.flag_image
        else:
            cell.label.config(image=self.blank_image, text="")
            cell.label.image = self.blank_image

    def game_over(self, win):
        for row in self.board:
            for cell in row:
                if cell.is_mine:
                    cell.label.config(image=self.mine_image, text="", compound='center')
                    cell.label.image = self.mine_image

        msg = "You Win!" if win else "Game Over!"
        self.popup(msg)

    def check_win(self):
        for row in self.board:
            for cell in row:
                if not cell.is_mine and not cell.is_revealed:
                    return
        self.game_over(True)

    def popup(self, msg):
        popup = tk.Toplevel()
        popup.title("Game Result")
        tk.Label(popup, text=msg, font=("Arial", 14)).pack(pady=10)
        tk.Button(popup, text="Exit", command=self.master.quit).pack(pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Minesweeper 9x12")
    game = Minesweeper(root)
    root.mainloop()

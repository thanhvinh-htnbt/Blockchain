import os
import tkinter as tk
from PIL import Image, ImageTk

ROWS = 3
COLS = 5
IMAGE_SIZE = 60

def write_path(path):
    with open("path.txt", "w") as f:
        f.write(path)

class Cell:
    def __init__(self, x, y, label, path):
        self.x = x
        self.y = y
        self.label = label
        self.is_using = False
        self.path = path

class Storage:
    def __init__(self, master, menu_root):
        self.master = master
        self.menu_root = menu_root
        self.board = []
        self.image_cache = []

        # Load all available image paths from folder
        self.image_paths = sorted([
            f"../collection/img_flag_{i}.png"
            for i in range(1, ROWS * COLS + 1)
            if os.path.exists(f"../collection/img_flag_{i}.png")
        ])

        self.blank_image = ImageTk.PhotoImage(Image.open("img_empty.png").resize((IMAGE_SIZE, IMAGE_SIZE)))
        self.setup(ROWS, COLS)

    def setup(self, ROWS, COLS):
        img_index = 0
        for x in range(ROWS):
            row = []
            for y in range(COLS):
                if img_index < len(self.image_paths):
                    path = self.image_paths[img_index]
                    img = Image.open(path).resize((IMAGE_SIZE, IMAGE_SIZE))
                    photo = ImageTk.PhotoImage(img)
                    self.image_cache.append(photo)
                else:
                    path = ""
                    photo = self.blank_image

                label = tk.Label(self.master, image=photo, width=IMAGE_SIZE, height=IMAGE_SIZE)
                label.image = photo
                label.grid(row=x, column=y)

                cell = Cell(x, y, label, path)
                label.bind("<Button-1>", lambda e, c=cell: self.choose(c))
                row.append(cell)
                img_index += 1
            self.board.append(row)


    def choose(self, cell):
        if cell.is_using:
            return
        write_path(cell.path)

        self.popup("Are sure to choose this item?")



    def popup(self, msg):
        popup = tk.Toplevel()
        popup.title("Choose Item")
        tk.Label(popup, text=msg, font=("Arial", 14)).pack(pady=10)

        def return_to_menu():
            popup.destroy()
            self.master.destroy()
            self.menu_root.deiconify()

        def return_to_storage():
            popup.destroy()

        tk.Button(popup, text="OK", command=return_to_menu).pack(pady=5)
        tk.Button(popup, text="Cancel", command=return_to_storage).pack(pady=5)
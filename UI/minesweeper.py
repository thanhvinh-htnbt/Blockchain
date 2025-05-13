import tkinter as tk
from PIL import Image, ImageTk
import random
from web3 import Web3
import json
from config.config import GANACHE_URL, CONTRACT_ADDRESS
from UI import main

IMAGE_SIZE = 30

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
    def __init__(self, master, MODE, menu_root):
        self.master = master
        self.menu_root = menu_root
        self.board = []
        self.reward = 0


        if MODE == "EASY":
            ROWS = 4
            COLS = 6
            MINES = 3
            self.reward = 50
        elif MODE == "MEDIUM":
            ROWS = 9
            COLS = 12
            MINES = 20
            self.reward = 100
        elif MODE == "HARD":
            ROWS = 12
            COLS = 18
            MINES = 50
            self.reward = 200

        main.center_window(self.master, COLS*(IMAGE_SIZE+4), ROWS*(IMAGE_SIZE+4))

        with open("path.txt", "r") as file:
            path = file.read()

        self.blank_image = ImageTk.PhotoImage(Image.open("../block/img_blank.png").resize((IMAGE_SIZE, IMAGE_SIZE)))
        self.flag_image = ImageTk.PhotoImage(Image.open(path).resize((IMAGE_SIZE, IMAGE_SIZE)))
        self.mine_image = ImageTk.PhotoImage(Image.open("../block/img_mine.png").resize((IMAGE_SIZE, IMAGE_SIZE)))
        self.empty_image = ImageTk.PhotoImage(Image.open("../block/img_0.png").resize((IMAGE_SIZE, IMAGE_SIZE)))
        self.number_images = {}
        for i in range(1, 8):
            img = Image.open(f"../block/img_{i}.png").resize((IMAGE_SIZE, IMAGE_SIZE))
            self.number_images[i] = ImageTk.PhotoImage(img)

        self.setup(ROWS, COLS, MINES)

    def setup(self, ROWS, COLS, MINES):
        for x in range(ROWS):
            row = []
            for y in range(COLS):
                label = tk.Label(self.master, image=self.blank_image, width=IMAGE_SIZE, height=IMAGE_SIZE)
                label.image = self.blank_image
                label.grid(row=x, column=y, padx=0, pady=0)

                cell = Cell(x, y, label)
                label.bind("<Button-1>", lambda e, c=cell: self.reveal(c, ROWS, COLS))
                label.bind("<Button-3>", lambda e, c=cell: self.flag(c))
                row.append(cell)
            self.board.append(row)

        self.place_mines(ROWS, COLS, MINES)
        self.calculate_neighbors(ROWS, COLS)

    def place_mines(self, ROWS, COLS, MINES):
        count = 0
        while count < MINES:
            x = random.randint(0, ROWS - 1)
            y = random.randint(0, COLS - 1)
            cell = self.board[x][y]
            if not cell.is_mine:
                cell.is_mine = True
                count += 1

    def calculate_neighbors(self, ROWS, COLS):
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

    def reveal(self, cell, ROWS, COLS):
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
                cell.label.config(image=self.empty_image)
                cell.label.image = self.empty_image

            if cell.neighbor_mines == 0:
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        nx, ny = cell.x + dx, cell.y + dy
                        if 0 <= nx < ROWS and 0 <= ny < COLS:
                            neighbor = self.board[nx][ny]
                            if not neighbor.is_revealed:
                                self.reveal(neighbor, ROWS, COLS)
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

        msg = ""

        if win:
            msg = f"You Win!\nYou have received f{self.reward} coins"
            self.send_reward()
        else:
            msg = "Game Over!"

        self.popup(msg)

    def send_reward(self):
        w3 = Web3(Web3.HTTPProvider(GANACHE_URL))
        print("Kết nối:", w3.is_connected())

        # Đọc thông tin tài khoản từ file JSON
        with open("../scripts/accounts.json", "r") as f:
            accounts = json.load(f)

        sender = accounts[0]
        receiver = accounts[1]

        tx = {
            'nonce': w3.eth.get_transaction_count(sender["address"]),
            'to': receiver["address"],
            'value': w3.to_wei(self.reward, 'ether'),
            'gas': 21000,
            'gasPrice': w3.to_wei('50', 'gwei')
        }

        # Ký và gửi transaction
        signed_tx = w3.eth.account.sign_transaction(tx, sender["private_key"])
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

        balance_sender = w3.from_wei(w3.eth.get_balance(sender["address"]), 'ether')
        balance_receiver = w3.from_wei(w3.eth.get_balance(receiver["address"]), 'ether')
        print(f"Số dư người gửi: {balance_sender} ETH")
        print(f"Số dư người nhận: {balance_receiver} ETH")


    def check_win(self):
        for row in self.board:
            for cell in row:
                if not cell.is_mine and not cell.is_revealed:
                    return
        self.game_over(True)

    def popup(self, msg):
        popup = tk.Toplevel()
        popup.title("Game Result")
        main.center_window(popup, 250, 120)
        tk.Label(popup, text=msg, font=("Arial", 14)).pack(pady=10)

        def return_to_menu():
            popup.destroy()
            self.master.destroy()
            self.menu_root.deiconify()

        tk.Button(popup, text="Exit", command=return_to_menu).pack(pady=5)




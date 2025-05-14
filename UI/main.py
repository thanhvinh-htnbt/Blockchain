import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont
import NFTsStore
from web3 import Web3
import json
import minesweeper
import storage
import blockchain

from deploy import deploy


def create_canvas_button(image_path, text, x, y, command):
    image = Image.open(image_path).convert("RGBA")
    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype("arial.ttf", 18)
    except:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    draw.text(
        ((image.width - text_width) / 2, (image.height - text_height) / 2),
        text, fill="white", font=font
    )

    photo = ImageTk.PhotoImage(image)
    img_id = canvas.create_image(x, y, image=photo)
    canvas.image_store.append(photo)

    def is_inside(event_x, event_y):
        return (x - image.width // 2 <= event_x <= x + image.width // 2 and
                y - image.height // 2 <= event_y <= y + image.height // 2)

    def on_click(event):
        if is_inside(event.x, event.y):
            command()

    canvas.tag_bind(img_id, "<Button-1>", on_click)

def start_game(difficulty):
    root.withdraw()
    game_window = tk.Toplevel()
    game_window.title(f"Minesweeper - {difficulty}")
    game = minesweeper.Minesweeper(game_window, difficulty, root)

def choose_difficulty():
    diff_win = tk.Toplevel()
    diff_win.title("Select Difficulty")
    center_window(diff_win, 250, 200)

    tk.Label(diff_win, text="Choose Difficulty:", font=("Arial", 12)).pack(pady=10)

    for level in ["EASY", "MEDIUM", "HARD"]:
        tk.Button(diff_win, text=level, width=10, bg="#4CAF50", fg="white", font=("Arial", 10),
                  command=lambda lvl=level: [diff_win.destroy(), start_game(lvl)]
                  ).pack(pady=5)

def open_shop(user_address, private_key):
    root.withdraw()
    shop_window = tk.Toplevel()
    shop_window.title(f"Storage")
    NFTsStore.NFTsStore(user_address, private_key, shop_window, root)

    

def center_window(win, width, height):
    win.update_idletasks()
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    win.geometry(f"{width}x{height}+{x}+{y}")


def open_storage():
    root.withdraw()
    storage_window = tk.Toplevel()
    storage_window.title(f"NFT Marketplace")
    storage.Storage(storage_window, root)

def open_blockchain():
    root.withdraw()
    blockchain_window = tk.Toplevel()
    blockchain_window.title(f"BLock Viewer")
    blockchain.BlockViewer(blockchain_window, root)

def deploy_contract():
    w3, contract, server = deploy.deploy()
    messagebox.showinfo("Deplou contract thành công", f"Contract đã được triển khai tại: {contract.address}")



if __name__ == '__main__':

    with open("../config/config.json", "r") as f:
        config = json.load(f)

    ganache_url = config["GANACHE_URL"]
    w3 = Web3(Web3.HTTPProvider(ganache_url))

    with open("../scripts/accounts.json", "r") as f:
        accounts = json.load(f)

    server = accounts[0]
    user = accounts[1]
    user_address = user["address"]
    user_private_key = user["private_key"]
    root = tk.Tk()
    root.title("Main Menu")
    center_window(root, 600, 400)

    bg_image = Image.open("img_background.png").resize((600, 400))
    bg_photo = ImageTk.PhotoImage(bg_image)

    canvas = tk.Canvas(root, width=600, height=400, highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=bg_photo, anchor='nw')

    canvas.create_text(300, 50, text="Minesweeper", font=("Arial", 22, "bold"), fill="#CB0404")

    canvas.image_store = []

    create_canvas_button("button.png", "Play", 300, 120, choose_difficulty)
    create_canvas_button("button.png", "Shop", 300, 180, lambda: open_shop(user_address, user_private_key))
    create_canvas_button("button.png", "Storage", 300, 240, open_storage)
    create_canvas_button("button.png", "Blockchain", 300, 300, open_blockchain)
    create_canvas_button("button.png", "Deploy", 300, 360, deploy_contract)
    root.mainloop()

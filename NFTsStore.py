import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from scripts.mint_NFT import mint_nft
import os
import json

# Cấu hình
NFT_FOLDER = "NFTsData"
PRICES_FILE = "prices.json"

bought_nfts = set()

# Hàm xử lý khi nhấn nút Mua
def buy_nft(image_path, buy_button):
    if image_path in bought_nfts:
        messagebox.showinfo("Đã mua", "Bạn đã mua NFT này rồi.")
        return

    try:
        with open(image_path, "rb") as f:
            image_data = f.read()

        # Gọi hàm mint NFT
        mint_nft(image_data)

        # Đánh dấu là đã mua
        bought_nfts.add(image_path)
        buy_button.config(state="disabled", text="Đã mua")
        messagebox.showinfo("Thành công", "Mua NFT thành công!")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Mua NFT thất bại:\n{e}")

# Hàm tạo giao diện
def load_nfts(root):
    nft_folder = "NFTsData"
    files = os.listdir(nft_folder)
    images = [f for f in files if f.lower().endswith((".png", ".jpg", ".jpeg"))]

    row = 0
    col = 0
    for img_file in images:
        frame = tk.Frame(root, padx=10, pady=10)
        frame.grid(row=row, column=col)

        img_path = os.path.join(nft_folder, img_file)
        pil_image = Image.open(img_path).resize((150, 150))
        tk_image = ImageTk.PhotoImage(pil_image)

        label = tk.Label(frame, image=tk_image)
        label.image = tk_image  # Giữ tham chiếu tránh bị garbage collected
        label.pack()

        price = tk.Label(frame, text="Giá: 1 ETH", font=("Arial", 12))
        price.pack()

        buy_button = tk.Button(frame, text="Mua")
        buy_button.config(command=lambda p=img_path, b=buy_button: buy_nft(p, b))
        buy_button.pack()

        col += 1
        if col >= 3:
            row += 1
            col = 0
    

if __name__ == "__main__":
    root = tk.Tk()
    root.title("NFT Marketplace")
    load_nfts(root)
    root.mainloop()

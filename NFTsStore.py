import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
from scripts.mint_NFT import mint_nft
import os
import json
import base64

NFT_FOLDER = "NFTsData"
PRICES_FILE = "prices.json"
bought_nfts = set()

# Load giá từ prices.json
def load_prices():
    if os.path.exists(PRICES_FILE):
        with open(PRICES_FILE, "r") as f:
            return json.load(f)
    return {}

# Hàm chuyển ảnh thành tokenURI base64
def image_to_data_uri(image_path):
    ext = os.path.splitext(image_path)[1].lower()
    mime_type = "image/jpeg"
    if ext == ".png":
        mime_type = "image/png"

    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode("utf-8")
    return f"data:{mime_type};base64,{encoded}"

# Hàm xử lý khi nhấn nút Mua
def buy_nft(image_path, button, recipient_address, private_key):
    if image_path in bought_nfts:
        messagebox.showinfo("Đã mua", "Bạn đã mua NFT này rồi.")
        return

    try:
        token_uri = image_to_data_uri(image_path)
        mint_nft(token_uri, recipient_address, private_key)  # Gửi base64 vào contract

        bought_nfts.add(image_path)
        button.config(state="disabled", text="Đã mua")
        messagebox.showinfo("Thành công", "Mua NFT thành công!")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Mua NFT thất bại:\n{e}")

# Load ảnh và tạo giao diện
def load_nfts(container, recipient_address, private_key):
    prices = load_prices()
    files = os.listdir(NFT_FOLDER)
    images = [f for f in files if f.lower().endswith((".png", ".jpg", ".jpeg"))]

    row = 0
    col = 0
    for img_file in images:
        img_path = os.path.join(NFT_FOLDER, img_file)

        frame = ttk.Frame(container, padding=10)
        frame.grid(row=row, column=col, sticky="n")

        pil_image = Image.open(img_path).resize((150, 150))
        tk_image = ImageTk.PhotoImage(pil_image)

        img_label = ttk.Label(frame, image=tk_image)
        img_label.image = tk_image
        img_label.pack()

        price_val = prices.get(img_file, "1 ETH")
        price_label = ttk.Label(frame, text=f"Giá: {price_val}", font=("Arial", 12))
        price_label.pack()

        buy_button = ttk.Button(frame, text="Mua")
        buy_button.config(command=lambda path=img_path, btn=buy_button: buy_nft(path, btn, recipient_address, private_key))
        buy_button.pack()

        col += 1
        if col >= 3:
            row += 1
            col = 0

# Giao diện chính
def main():
    recipient_address = "0x254228Db98670755cba6a17DAee3AB732ab68130"  # <- thay địa chỉ ví
    private_key = "0x2aef5894f2988c7b498327b8d0d3fa9ced010b3ced9576ac991b45e87747f737"  # <- thay khóa riêng

    root = tk.Tk()
    root.title("NFT Marketplace")

    canvas = tk.Canvas(root)
    scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scroll_frame = ttk.Frame(canvas)

    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    load_nfts(scroll_frame, recipient_address, private_key)
    root.mainloop()

if __name__ == "__main__":
    main()

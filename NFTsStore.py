import tkinter as tk
import os
import io
import json
import base64
import shutil
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
from scripts.mint_NFT import mint_nft
from PIL import Image


NFT_FOLDER = "NFTsData"
PRICES_FILE = "NFTsData/prices.json"
COLLECTION = "collection"

# Load giá từ prices.json
def load_prices():
    if os.path.exists(PRICES_FILE):
        with open(PRICES_FILE, "r") as f:
            return json.load(f)
    return {}

def data_uri_to_image(data_uri):
    header, encoded = data_uri.split(",", 1)
    image_data = base64.b64decode(encoded)
    image = Image.open(io.BytesIO(image_data))
    return image

# Hàm chuyển ảnh thành tokenURI base64
def image_to_data_uri(image_path):
    ext = os.path.splitext(image_path)[1].lower()
    mime_type = "image/jpeg"
    if ext == ".png":
        mime_type = "image/png"

    with Image.open(image_path) as img:
        img = img.resize((50, 50))  # Resize về 50x50

        # Lưu ảnh vào bộ nhớ thay vì file
        buffer = io.BytesIO()
        format = "PNG" if mime_type == "image/png" else "JPEG"
        img.save(buffer, format=format)
        encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return f"data:{mime_type};base64,{encoded}"

# Hàm xử lý khi nhấn nút Mua
def buy_nft(image_path, button, recipient_address, private_key, price_eth):

    file_name = os.path.basename(image_path)
    collection_path = os.path.join(COLLECTION, file_name)

    
    if os.path.exists(collection_path):
        messagebox.showinfo("Đã mua", "Bạn đã mua NFT này rồi.")
        return

    try:
        token_uri_input = image_to_data_uri(image_path)

        # Mint NFT và nhận lại tokenURI thực tế từ blockchain
        token_uri_onchain = mint_nft(token_uri_input, recipient_address, private_key, price_eth)

        # Giải mã lại ảnh từ tokenURI
        image = data_uri_to_image(token_uri_onchain)

        if not os.path.exists(COLLECTION):
            os.makedirs(COLLECTION)


        save_path = os.path.join(COLLECTION, file_name)
        image.save(save_path)
        button.config(state="disabled", text="Đã mua")
        messagebox.showinfo("Thành công", "Mua NFT thành công!")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Mua NFT thất bại:\n{e}")

# Load ảnh và tạo giao diện
def load_nfts(container, user_address, private_key):
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
        buy_button.config(command=lambda path=img_path, btn=buy_button: 
                            buy_nft(path, btn, user_address, private_key, price_val))
        buy_button.pack()

        col += 1
        if col >= 3:
            row += 1
            col = 0


# Giao diện chính
def show_nft_store(user_address, private_key):
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

    load_nfts(scroll_frame, user_address, private_key)
    root.mainloop()





if __name__ == "__main__":
    show_nft_store("0x254228Db98670755cba6a17DAee3AB732ab68130", "0x2aef5894f2988c7b498327b8d0d3fa9ced010b3ced9576ac991b45e87747f737")

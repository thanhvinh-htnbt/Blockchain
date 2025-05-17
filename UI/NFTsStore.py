import tkinter as tk
import os
import io
import json
import base64
from tkinter import messagebox, ttk
from PIL import ImageTk
from scripts import mint_NFT
from PIL import Image
from web3 import Web3


NFT_FOLDER = "../NFTsData"
PRICES_FILE = "../NFTsData/prices.json"
COLLECTION = "../collection"

class NFTsStore:
    def __init__(self, user_address, private_key, master, menu_root):
        self.master = master
        self.menu_root = menu_root

        with open("../config/config.json", "r") as f:
            config = json.load(f)

        ganache_url = config["GANACHE_URL"]
        self.w3 = Web3(Web3.HTTPProvider(ganache_url))
        self.user_address = user_address

        main_frame = ttk.Frame(master)
        main_frame.pack(fill="both", expand=True)

        # Label hiển thị số dư
        balance = self.get_eth_balance()
        self.balance_label = ttk.Label(main_frame, text=f"Số dư: {balance} ETH", font=("Arial", 14, "bold"))
        self.balance_label.pack(anchor="nw", padx=10, pady=5)

        canvas = tk.Canvas(main_frame, width=1200, height=700)  # ➕ rộng hơn
        x_scrollbar = ttk.Scrollbar(main_frame, orient="horizontal", command=canvas.xview)
        y_scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)

        scroll_frame = ttk.Frame(canvas)

        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

        canvas.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        y_scrollbar.pack(side="right", fill="y")
        x_scrollbar.pack(side="bottom", fill="x")

        # Load NFTs
        self.load_nfts(scroll_frame, user_address, private_key)

        self.master.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        self.master.destroy()
        self.menu_root.deiconify()

    # Load giá từ prices.json
    def load_prices(self):
        if os.path.exists(PRICES_FILE):
            with open(PRICES_FILE, "r") as f:
                return json.load(f)
        return {}

    def data_uri_to_image(self, data_uri):
        header, encoded = data_uri.split(",", 1)
        image_data = base64.b64decode(encoded)
        image = Image.open(io.BytesIO(image_data))
        return image

    # Hàm chuyển ảnh thành tokenURI base64
    def image_to_data_uri(self, image_path):
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
    def buy_nft(self, image_path, button, recipient_address, private_key, price_eth):

        print(price_eth)

        file_name = os.path.basename(image_path)
        collection_path = os.path.join(COLLECTION, file_name)

        if os.path.exists(collection_path):
            messagebox.showinfo("Đã mua", "Bạn đã mua NFT này rồi.")
            return

        try:
            token_uri_input = self.image_to_data_uri(image_path)

            # Mint NFT và nhận lại tokenURI thực tế từ blockchain
            token_uri_onchain = mint_NFT.mint_nft(token_uri_input, recipient_address, private_key, price_eth)

            # Giải mã lại ảnh từ tokenURI
            image = self.data_uri_to_image(token_uri_onchain)

            if not os.path.exists(COLLECTION):
                os.makedirs(COLLECTION)

            save_path = os.path.join(COLLECTION, file_name)
            image.save(save_path)
            button.config(state="disabled", text="Đã mua")
            messagebox.showinfo("Thành công", "Mua NFT thành công!")

            new_balance = self.get_eth_balance()
            self.balance_label.config(text=f"Số dư: {new_balance} ETH")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Mua NFT thất bại:\n{e}")

    def get_eth_balance(self):
        try:
            balance_wei = self.w3.eth.get_balance(self.user_address)
            balance_eth = self.w3.from_wei(balance_wei, 'ether')
            return round(balance_eth, 4)
        except Exception as e:
            print(f"Lỗi khi lấy số dư: {e}")
            return 0

    # Load ảnh và tạo giao diện
    def load_nfts(self, container, user_address, private_key):
        prices = self.load_prices()
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

            file_name = os.path.basename(img_path)
            collection_path = os.path.join(COLLECTION, file_name)
            buy_button = ttk.Button(frame, text="Mua")

            if os.path.exists(collection_path):
                buy_button.config(state="disabled", text="Đã mua")
            else:
                buy_button.config(command=lambda path=img_path, btn=buy_button, price = price_val:
                self.buy_nft(path, btn, user_address, private_key, price))
            
            buy_button.pack()
                

            col += 1
            if col >= 3:
                row += 1
                col = 0





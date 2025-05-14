import json
import tkinter as tk
from datetime import datetime

from web3 import Web3


class BlockViewer:
    def __init__(self, master, menu_root):
        self.master = master
        self.menu_root = menu_root

        # Scrollable canvas area
        canvas = tk.Canvas(self.master)
        scrollbar = tk.Scrollbar(self.master, orient="vertical", command=canvas.yview)
        self.block_frame = tk.Frame(canvas)

        self.block_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.block_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.load_blocks()

        self.master.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        self.master.destroy()
        self.menu_root.deiconify()

    def get_block_info(self, start=0, end=None):
        with open("../config/config.json", "r") as f:
            config = json.load(f)

        ganache_url = config["GANACHE_URL"]
        w3 = Web3(Web3.HTTPProvider(ganache_url))
        if end is None:
            end = w3.eth.block_number
        blocks = []
        for i in range(start, end + 1):
            block = w3.eth.get_block(i, full_transactions=True)
            blocks.append(block)
        return blocks

    def load_blocks(self):
        blocks = self.get_block_info()

        for block in blocks:
            self.add_block_card(block)

    def add_block_card(self, block):
        timestamp = datetime.fromtimestamp(block.timestamp).strftime('%Y-%m-%d %H:%M:%S')
        frame = tk.Frame(self.block_frame, bd=2, relief="groove", padx=10, pady=5, bg="#f0f0f0")
        frame.pack(fill="x", pady=3, padx=5)

        label = tk.Label(frame, text=f"Block #{block.number} - {timestamp}", font=("Arial", 12, "bold"), bg="#f0f0f0")
        label.pack(anchor="w")

        sublabel = tk.Label(frame, text=f"Hash: {block.hash.hex()[:20]}... | TXs: {len(block.transactions)}",
                            bg="#f0f0f0")
        sublabel.pack(anchor="w")

        frame.bind("<Button-1>", lambda e, b=block: self.show_block_detail(b))
        label.bind("<Button-1>", lambda e, b=block: self.show_block_detail(b))
        sublabel.bind("<Button-1>", lambda e, b=block: self.show_block_detail(b))

    def show_block_detail(self, block):
        detail_window = tk.Toplevel()
        detail_window.title(f"Block #{block.number} Details")
        detail_window.geometry("700x200")

        text_widget = tk.Text(detail_window, wrap="word", font=("Courier", 10))
        text_widget.pack(expand=True, fill="both")

        detail_lines = [
            f"{'Block Number:':20} {block.number}",
            f"{'Hash:':20} {block.hash.hex()}",
            f"{'Parent Hash:':20} {block.parentHash.hex()}",
            f"{'Timestamp:':20} {datetime.fromtimestamp(block.timestamp)}",
            f"{'Miner:':20} {block.miner}",
            f"{'Difficulty:':20} {block.difficulty}",
            f"{'Gas Used:':20} {block.gasUsed}",
            f"{'Gas Limit:':20} {block.gasLimit}",
            f"{'Transactions:':20} {len(block.transactions)}",
        ]

        for line in detail_lines:
            text_widget.insert(tk.END, line + "\n")

        text_widget.config(state="disabled")



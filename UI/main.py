import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageFont
import minesweeper
import storage


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

def open_shop():
    return

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
    storage_window.title(f"Storage")
    storage.Storage(storage_window, root)

def open_blockchain():
    return

if __name__ == '__main__':
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
    create_canvas_button("button.png", "Shop", 300, 180, open_shop)
    create_canvas_button("button.png", "Storage", 300, 240, open_storage)
    create_canvas_button("button.png", "Blockchain", 300, 300, open_blockchain)

    root.mainloop()

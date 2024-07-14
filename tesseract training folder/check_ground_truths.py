import os
import shutil
from PIL import Image, ImageTk
import tkinter as tk


def create_gui():
    """
    Create and run the GUI for checking ground truths.
    """
    ground_truths_dir = "unprocessed_ground_truths"
    screenshots_dir = "gold_screenshots"
    new_ground_truths_dir = "ground_truths"

    if not os.path.exists(new_ground_truths_dir):
        os.makedirs(new_ground_truths_dir)

    files = [f for f in os.listdir(ground_truths_dir) if f.endswith(".txt")]
    files.sort()

    if not files:
        print("No files to process.")
        return

    window = tk.Tk()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window.geometry(f"{screen_width}x{screen_height}")

    next_button = tk.Button(window, text="Next")
    next_button.pack(side="left")

    def load_image_and_text():
        img = Image.open(os.path.join(screenshots_dir, files[0][:-4] + ".png"))
        img = img.resize((screen_width // 2, screen_height - 50), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        panel.configure(image=img)
        panel.image = img
        with open(os.path.join(ground_truths_dir, files[0]), "r") as f:
            text.delete("1.0", "end")
            text.insert("1.0", f.read())

    img = Image.open(os.path.join(screenshots_dir, files[0][:-4] + ".png"))
    img = img.resize((screen_width // 2, screen_height - 50), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    panel = tk.Label(window, image=img)
    panel.pack(side="left", fill="both", expand="yes")

    text = tk.Text(window)
    with open(os.path.join(ground_truths_dir, files[0]), "r") as f:
        text.insert("1.0", f.read())
    text.pack(side="right", fill="both", expand="yes")

    def handle_click():
        with open(os.path.join(new_ground_truths_dir, files[0]), "w") as f:
            f.write(text.get("1.0", "end-1c"))
        shutil.copy(
            os.path.join(screenshots_dir, files[0][:-4] + ".png"),
            os.path.join(new_ground_truths_dir, files[0][:-4] + ".png"),
        )
        files.pop(0)
        if files:
            load_image_and_text()
        else:
            window.quit()

    next_button.configure(command=handle_click)
    window.mainloop()


if __name__ == "__main__":
    create_gui()

import os
import shutil
from PIL import Image, ImageTk
import tkinter as tk


def sort_photos():
    """
    Create and run the GUI for sorting photos.
    """
    unprocessed_dir = "raw_screenshots"
    processed_dir = "gold_screenshots"

    if not os.path.exists(processed_dir):
        os.makedirs(processed_dir)

    processed_files = [f for f in os.listdir(processed_dir) if f.endswith(".png")]
    processed_files.sort()

    for i, filename in enumerate(processed_files):
        os.rename(
            os.path.join(processed_dir, filename),
            os.path.join(processed_dir, f"screenshot_{i}.png"),
        )

    files = [f for f in os.listdir(unprocessed_dir) if f.endswith(".png")]
    files.sort()

    if not files:
        print("No files to process.")
        return

    window = tk.Tk()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window.geometry(f"{screen_width}x{screen_height}")

    yes_button = tk.Button(window, text="Yes")
    yes_button.pack(side="left")

    no_button = tk.Button(window, text="No")
    no_button.pack(side="right")

    img = Image.open(os.path.join(unprocessed_dir, files[0]))
    img = img.resize((screen_width, screen_height - 50), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    panel = tk.Label(window, image=img)
    panel.pack(side="bottom", fill="both", expand="yes")

    def handle_click(move):
        if move:
            processed_files = [
                f for f in os.listdir(processed_dir) if f.endswith(".png")
            ]
            new_filename = f"screenshot_{len(processed_files)}.png"
            shutil.move(
                os.path.join(unprocessed_dir, files[0]),
                os.path.join(processed_dir, new_filename),
            )
        else:
            os.remove(os.path.join(unprocessed_dir, files[0]))
        files.pop(0)
        if files:
            img2 = Image.open(os.path.join(unprocessed_dir, files[0]))
            img2 = img2.resize((screen_width, screen_height - 50), Image.ANTIALIAS)
            img2 = ImageTk.PhotoImage(img2)
            panel.configure(image=img2)
            panel.image = img2
        else:
            window.quit()

    yes_button.configure(command=lambda: handle_click(True))
    no_button.configure(command=lambda: handle_click(False))
    window.mainloop()


if __name__ == "__main__":
    sort_photos()

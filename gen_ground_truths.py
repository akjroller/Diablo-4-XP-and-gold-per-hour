import os
import pytesseract
from PIL import Image

source_folder = "gold_screenshots"
destination_folder = "unprocessed_ground_truths"

if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

for filename in os.listdir(source_folder):
    if filename.endswith(".png"):
        with Image.open(os.path.join(source_folder, filename)) as img:
            text = pytesseract.image_to_string(img)
            
            with open(os.path.join(destination_folder, filename[:-4] + ".txt"), "w") as text_file:
                text_file.write(text)

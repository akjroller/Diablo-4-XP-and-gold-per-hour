import os
from PIL import Image
import pytesseract


def generate_ground_truths(
    source_folder="gold_screenshots", destination_folder="unprocessed_ground_truths"
):
    """
    Generate text files from images using Tesseract OCR.
    :param source_folder: Folder containing source images.
    :param destination_folder: Folder to save generated text files.
    """
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    for filename in os.listdir(source_folder):
        if filename.endswith(".png"):
            with Image.open(os.path.join(source_folder, filename)) as img:
                text = pytesseract.image_to_string(img)
                with open(
                    os.path.join(destination_folder, filename[:-4] + ".txt"), "w"
                ) as text_file:
                    text_file.write(text)
                print(f"Generated text file for {filename}")


if __name__ == "__main__":
    generate_ground_truths()

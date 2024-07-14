import os
import subprocess


def generate_tesseract_files(data_dir="../ground_truths"):
    """
    Generate .box files for Tesseract training from images.
    :param data_dir: Directory containing ground truth images.
    """
    for filename in os.listdir(data_dir):
        if filename.endswith(".png"):
            base_filename = filename[:-4]
            image_file = os.path.join(data_dir, filename)
            command = [
                "tesseract",
                image_file,
                os.path.join(data_dir, base_filename),
                "-l",
                "eng",
                "--psm",
                "6",
                "makebox",
            ]
            try:
                subprocess.run(command, check=True)
                print(f"Generated .box file for {filename}")
            except subprocess.CalledProcessError as e:
                print(f"Error processing {filename}: {e}")


if __name__ == "__main__":
    generate_tesseract_files()

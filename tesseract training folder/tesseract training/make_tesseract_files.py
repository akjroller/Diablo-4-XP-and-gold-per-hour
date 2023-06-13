import os
import subprocess

data_dir = "../ground_truths"

for filename in os.listdir(data_dir):
    if filename.endswith(".png"):
        base_filename = filename[:-4]
        image_file = os.path.join(data_dir, filename)

        command = [
            'tesseract',
            image_file,
            os.path.join(data_dir, base_filename),
            '-l', 'eng',
            '--psm', '6',
            'makebox'
        ]
        subprocess.run(command, check=True)

# Contributing to Diablo 4 Gold and XP per Hour Project

First off, thank you for considering contributing to this project! All types of contributions are encouraged and valued.

## Getting Started

This project aims to develop a system that automatically identifies the presence of gold and XP in Diablo 4, then estimates the gold and XP earning rate. The main tasks involved are gathering screenshots and their corresponding ground truths to train a Tesseract model.

### Step 1

Clone the repository and install the necessary Python packages. These include NumPy, OpenCV, mss, PIL (Pillow), Tkinter, and PyTesseract.

### Step 2

Run the `take_screen_shots.py` script to start gathering screenshots. Ensure you adjust the screen area to match your game's window. The screenshots will be saved in the `raw_screenshots` directory.

### Step 3

Execute the `sort_photos.py` script. This script provides a GUI where you can see each screenshot one at a time. If you find gold or XP in the screenshot, click "Yes" to move the screenshot to the `gold_screenshots` directory. If not, click "No" to delete the screenshot.

### Step 4

Run the `gen_ground_truths.py` script to generate ground truths for each screenshot in the `gold_screenshots` directory. The script uses PyTesseract to extract text and writes it into corresponding files in the `unprocessed_ground_truths` directory.

### Step 5

Manually verify and correct each ground truth file in the `unprocessed_ground_truths` directory to ensure it matches the text in the corresponding image.

Once you have finished these steps, commit your changes and create a pull request.

## Pull Request Process

1. Ensure any install or build dependencies are removed before the end of the layer when doing a build.
2. Update the README.md with details of changes to the interface.

Remember to always respect all contributors and ensure a positive and professional environment. Happy contributing!

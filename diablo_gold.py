import PySimpleGUI as sg
import cv2
import numpy as np
import pytesseract
from mss import mss
import time
import re
import logging

# Set the Tesseract executable path if it's not in your PATH
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Update this path if needed
)


def select_screen_size():
    """
    Function to select the screen size from a predefined set.
    """
    screen_sizes = {"1080p": {"top": 100, "left": 400, "width": 1020, "height": 750}}

    layout = [
        [sg.Text("Select your screen size:")],
        [sg.Combo(list(screen_sizes.keys()), key="-SCREEN_SIZE-", size=(20, 1))],
        [sg.Button("OK")],
    ]

    window = sg.Window(
        "Screen Size Selection",
        layout,
        resizable=True,
        grab_anywhere=True,
        icon="icons/d4gold.ico",
    )

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, "OK"):
            break

    window.close()
    return screen_sizes.get(values["-SCREEN_SIZE-"])


def preprocess_image(image):
    """
    Preprocess the image to improve OCR accuracy.
    """
    grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Enhance the image by adjusting brightness and contrast
    enhanced = cv2.convertScaleAbs(grayscale, alpha=1.5, beta=0)
    # Apply thresholding to binarize the image
    _, thresholded = cv2.threshold(
        enhanced, 120, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )
    return thresholded


def get_gold_from_screen(mon, sct):
    """
    Function to capture the screen and extract gold amount using OCR.
    """
    screenshot = np.array(sct.grab(mon))
    processed_image = preprocess_image(screenshot)
    text = pytesseract.image_to_string(processed_image, config="--psm 11")

    gold_amount = 0
    logging.debug(f"OCR Text: {text}")
    if "Gold" in text:
        try:
            gold_amount = int(re.findall(r"Gold\s*(\d+)", text)[0])
            logging.info(f"{gold_amount} gold found on screen.")
        except (IndexError, ValueError):
            logging.warning("Could not parse gold amount")
    else:
        logging.info("No gold found on screen.")

    return gold_amount


def calculate_gold_per_hour(gold_list, decay_rate):
    """
    Function to calculate weighted gold per hour.
    """
    weights = [decay_rate**i for i in range(len(gold_list))]
    weights = [weight / sum(weights) for weight in weights]
    weighted_gold_per_minute = sum(g * w for g, w in zip(gold_list, weights))
    return weighted_gold_per_minute * 60


def main():
    logging.basicConfig(
        level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    mon = select_screen_size()
    if mon is None:
        logging.error("Invalid screen size selected.")
        return

    sct = mss()
    gold_list = []
    decay_rate = 0.9

    layout = [
        [sg.Text("Estimated gold per hour: "), sg.Text(size=(15, 1), key="-OUTPUT-")]
    ]
    window = sg.Window(
        "Gold Per Hour",
        layout,
        finalize=True,
        resizable=True,
        grab_anywhere=True,
        size=(500, 500),
        icon="icons/d4gold.ico",
    )

    start_time = time.time()

    while True:
        gold_current_second = get_gold_from_screen(mon, sct)
        gold_list.append(gold_current_second)

        if time.time() - start_time >= 60:
            gold_per_hour = calculate_gold_per_hour(gold_list, decay_rate)
            logging.info(f"Estimated gold per hour: {gold_per_hour}")
            window["-OUTPUT-"].update(f"{gold_per_hour:.2f}")

            gold_list = []
            start_time = time.time()
        else:
            time.sleep(0.1)

        event, _ = window.read(timeout=10)
        if event == sg.WIN_CLOSED:
            break

    window.close()


if __name__ == "__main__":
    main()

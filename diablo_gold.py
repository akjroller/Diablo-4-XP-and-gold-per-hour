import cv2
import numpy as np
import pytesseract
from mss import mss
import time
import re

mon = {'top': 0, 'left': 0, 'width': 1920, 'height': 1080}  # Adjust this to your screen
sct = mss()

def get_gold_from_screen():
    screenshot = np.array(sct.grab(mon))
    grayscale = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(grayscale, config='--psm 11')

    gold_amount = 0
    if "Gold" in text:
        try:
            gold_amount = int(re.findall(r'(\d+)\s*Gold', text)[0])
            print(f"{gold_amount} gold found on screen.")
        except (IndexError, ValueError):
            print("Could not parse gold amount")
    else:
        print("No gold found on screen.")

    return gold_amount

def main():
    gold_list = []
    weights = []
    decay_rate = 0.9 

    start_time = time.time()

    while True:
        gold_current_second = get_gold_from_screen()
        gold_list.append(gold_current_second)
        weights.append(decay_rate ** len(gold_list))

        if time.time() - start_time >= 60:
            weights = [weight / sum(weights) for weight in weights]

            weighted_gold_per_minute = sum(g * w for g, w in zip(gold_list, weights))
            gold_per_hour = weighted_gold_per_minute * 60

            print(f"Estimated gold per hour: {gold_per_hour}")

            gold_list = []
            weights = []
            start_time = time.time()
        else:
            time.sleep(1)

if __name__ == "__main__":
    main()

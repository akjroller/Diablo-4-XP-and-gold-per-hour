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
    text = pytesseract.image_to_string(screenshot, config='--psm 11')

   # print(f"OCR output: {text}")  # Debugging print statement

    gold_amount = 0
    if "Gold" in text:
        try:
            gold_amount = int(re.findall(r'(\d+)\s*Gold', text)[0])
            print(f"{gold_amount} gold found on screen.")  # Debugging print statement
        except (IndexError, ValueError):
            print("Could not parse gold amount")
    else:
        print("No gold found on screen.")

    return gold_amount

def main():
    total_gold = 0
    minutes = 0
    start_time = time.time()

    while True:
        gold_current_second = get_gold_from_screen()
        total_gold += gold_current_second

        if time.time() - start_time >= 60:  # 60 seconds (1 minute) have passed
            minutes += 1
            
            gold_per_minute = total_gold / minutes
            gold_per_hour = gold_per_minute * 60
            
            print(f"Estimated gold per hour: {gold_per_hour}")

            # reset total gold and start time for the next interval
            total_gold = 0
            start_time = time.time()
        else:
            time.sleep(1)  # wait for 1 second

if __name__ == "__main__":
    main()


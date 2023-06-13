import PySimpleGUI as sg
import cv2
import numpy as np
import pytesseract
from mss import mss
import time
import re


def select_screen_size():
    screen_sizes = {
        "1080p": {'top': 100, 'left': 400, 'width': 1020, 'height': 750}
    }

    layout = [[sg.Text("Select your screen size:")],
              [sg.Combo(list(screen_sizes.keys()), key='-SCREEN_SIZE-', size=(20, 1))],
              [sg.Button("OK")]]

    window = sg.Window('Screen Size Selection', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'OK':
            break

    window.close()
    return screen_sizes.get(values['-SCREEN_SIZE-'])
        

def get_gold_from_screen(mon, sct):
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
    mon = select_screen_size()
    if mon is None:
        print("Invalid screen size selected.")
        return

    sct = mss()
    gold_list = []
    weights = []
    decay_rate = 0.9 

    start_time = time.time()

    while True:
        gold_current_second = get_gold_from_screen(mon, sct)  # Passing mon and sct here
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

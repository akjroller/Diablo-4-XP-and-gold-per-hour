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

    window = sg.Window('Screen Size Selection', layout, resizable=True, grab_anywhere=True, icon='icons/d4gold.ico')

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
            gold_amount = int(re.findall(r'Gold\s*(\d+)', text)[0])
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

    layout = [[sg.Text("Estimated gold per hour: "), sg.Text(size=(15,1), key='-OUTPUT-')]]
    window = sg.Window('Gold Per Hour', layout, finalize=True, resizable=True, grab_anywhere=True, size=(500, 500), icon='icons/d4gold.ico')


    start_time = time.time()

    while True:
        gold_current_second = get_gold_from_screen(mon, sct)
        gold_list.append(gold_current_second)
        weights.append(decay_rate ** len(gold_list))

        if time.time() - start_time >= 60:
            weights = [weight / sum(weights) for weight in weights]

            weighted_gold_per_minute = sum(g * w for g, w in zip(gold_list, weights))
            gold_per_hour = weighted_gold_per_minute * 60

            print(f"Estimated gold per hour: {gold_per_hour}")
            window['-OUTPUT-'].update(f'{gold_per_hour:.2f}')

            gold_list = []
            weights = []
            start_time = time.time()
        else:
            time.sleep(0.1)

        event, values = window.read(timeout=10)
        if event == sg.WIN_CLOSED:
            break

    window.close()


if __name__ == "__main__":
    main()

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
    screen_size = None

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'OK':
            if event == 'OK':
                screen_size = screen_sizes.get(values['-SCREEN_SIZE-'])
            break

    window.close()
    return screen_size

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

def create_main_window():
    layout = [[sg.Text('Estimated gold per hour:'), sg.Text(size=(15,1), key='-OUTPUT-')]]
    return sg.Window('Diablo Gold Tracker', layout)

def update_gui(window, message):
    window['-OUTPUT-'].update(message)

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

    layout = [[sg.Text("Gold Detected:", size=(20,1), key='-GOLD_DETECTED-', justification='left')],
              [sg.Text("Estimated gold per hour:", size=(20,1), key='-ESTIMATED_GPH-', justification='left')],
              [sg.Button("Exit")]]


    window = sg.Window('Diablo Gold Tracker', layout, finalize=True, keep_on_top=True)

    while True:
        gold_current_second = get_gold_from_screen(mon, sct)
        gold_list.append(gold_current_second)
        weights.append(decay_rate ** len(gold_list))

        window['-GOLD_DETECTED-'].update(f"Gold Detected: {gold_current_second}")

        if time.time() - start_time >= 1:
            weights = [weight / sum(weights) for weight in weights]

            weighted_gold_per_minute = sum(g * w for g, w in zip(gold_list, weights))
            gold_per_hour = weighted_gold_per_minute * 60

            window['-ESTIMATED_GPH-'].update(f"Estimated gold per hour: {gold_per_hour}")

            gold_list = []
            weights = []
            start_time = time.time()

        event, values = window.read(timeout=100)
        if event == sg.WINDOW_CLOSED or event == 'Exit':
            break

    window.close()


if __name__ == "__main__":
    main()

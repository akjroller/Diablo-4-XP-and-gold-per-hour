import numpy as np
import cv2
import time
from mss import mss
import os

directory = "raw_screenshots"
if not os.path.exists(directory):
    os.makedirs(directory)

mon = {'top': 100, 'left': 400, 'width': 1020, 'height': 750}
sct = mss()

i = 0
while True:
    screenshot = np.array(sct.grab(mon))
    filename = os.path.join(directory, f"screenshot_{i}.png")

    cv2.imwrite(filename, cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR))

    print(f"Saved screenshot_{i}.png")
    i += 1

    time.sleep(1)

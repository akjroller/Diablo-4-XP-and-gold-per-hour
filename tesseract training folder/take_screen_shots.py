import os
import time
import cv2
import numpy as np
from mss import mss


def take_screenshots(directory="raw_screenshots", interval=1):
    """
    Take screenshots at regular intervals and save them to the specified directory.
    :param directory: Directory to save screenshots.
    :param interval: Interval between screenshots in seconds.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)

    mon = {"top": 100, "left": 400, "width": 1020, "height": 750}
    sct = mss()

    i = 0
    while True:
        screenshot = np.array(sct.grab(mon))
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
        filename = os.path.join(directory, f"screenshot_{i}.png")
        cv2.imwrite(filename, cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR))
        print(f"Saved {filename}")
        i += 1
        time.sleep(interval)


if __name__ == "__main__":
    take_screenshots()

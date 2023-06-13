# Warning! Running this could Violate Section 1.C.iii or Section 1.C.iv of Blizzard End User License Agreement Use at your OWN RISK
# This is still a work in progress and is not fully fuctional yet.
- It fails to detect the gold amount in the game most of the time.

# Diablo 4 Gold Tracker

This script uses Python and OCR (Optical Character Recognition) to take screenshots of your Diablo 4 game, parse the amount of gold you have, and estimate how much gold per hour you're earning.

## Dependencies

- Python 3.6 or higher
- Tesseract OCR
- Some Python libraries, including OpenCV, Numpy, Pytesseract, mss, Pillow, and Tkinter

## Installation

0. Install Tesseract: https://github.com/tesseract-ocr/tesseract

1. Clone this repository.

```bash
git clone https://github.com/your-github-username/diablo4-gold-tracker.git
```

2. Change into the directory.

```bash
cd diablo5-gold-tracker
```

3. Install the dependencies.

```bash
pip install -r requirements.txt
```


## Usage

### Windows Users

An executable version of the script is available in the main folder for ease of use.

Navigate to the main folder in the repository.
Double click the diablo_gold.exe file to run the application.

### Non-Windows Users

To start tracking gold, simply run the script.

```bash
python diablo_gold.py
```

The script will take screenshots every second and use OCR to read the gold amount. It calculates your estimated gold per hour and prints it out every minute.

Note: The 'mon' variable in the script defines the area of the screen the script will capture. You will need to adjust this to match the area of your screen where the gold amount is displayed in Diablo 4.

## To Do

- Improve the script's accuracy in detecting gold from the game. The OCR functionality can sometimes misread the on-screen text or fail to find it. Future enhancements should focus on refining this aspect of the script.

- Create .exe file for non-Windows users.

- Create a tesseract model for the gold font in the game.

- Make GUI more user friendly.

- Create an easier way for non technical users to install the .exe and dependencies.

- Make .exe and .py files more performant.


## Contributing

Contributions are welcome and appreciated! Please check out our [contributing guidelines](./CONTRIBUTING.md) for detailed information on how you can lend a hand.

# Diablo 4 Gold Tracker

This script uses Python and OCR (Optical Character Recognition) to take screenshots of your Diablo 4 game, parse the amount of gold you have, and estimate how much gold per hour you're earning.

## Dependencies

- Python 3.6 or higher
- OpenCV (cv2)
- Numpy
- Pytesseract
- mss
- Pillow
- Tkinter

## Installation

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

To start tracking gold, simply run the script.

```bash
python diablo_gold.py
```

The script will take screenshots every second and use OCR to read the gold amount. It calculates your estimated gold per hour and prints it out every minute.

Note: The 'mon' variable in the script defines the area of the screen the script will capture. You will need to adjust this to match the area of your screen where the gold amount is displayed in Diablo 4.

## To Do

- Improve the script's accuracy in detecting gold from the game. The OCR functionality can sometimes misread the on-screen text or fail to find it. Future enhancements should focus on refining this aspect of the script.


## Contributing

Contributions are welcome and appreciated! Please check out our [contributing guidelines](./CONTRIBUTING.md) for detailed information on how you can lend a hand.

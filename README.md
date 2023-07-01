# Valouncher

Valouncher is a script that allows you to manage and launch multiple accounts for the game Valorant.
It provides a simple command-line interface to add, edit, view, update rank information and launch accounts :)

## Prerequisites

Before using Valouncher, ensure that you have the following software/packages installed on your system:

- Python 3
- pywinauto
- pyautogui
- win32gui
- win32con

Or run to ensure that all required packages are installed:
```
pip install -r requirements.txt
```

## Installation

1. Clone this repository to your local machine or download the source code.
2. Navigate to the project directory.

## Usage

1. Open a terminal or command prompt.
2. Navigate to the project directory.
3. Run the script using the following command:

   ```bash
   python valouncher.py

## Why is 5.Fetch Account Details not working for me?

I have set by default for APAC region.
Please change "/ap/" to "/{your region}/"
your region can be any of these: na/latam/br/eu/kr/ap
```
LINE 323
def fetch_account_details():
    api_base_url = 'https://api.henrikdev.xyz/valorant/v1/mmr/ap/'
```

## Credits

Credits to Henrik-3 for sharing a Valorant API with us!
https://github.com/Henrik-3/unofficial-valorant-api

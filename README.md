# Valouncher

Valouncher is a script that allows you to manage and launch multiple accounts for the game Valorant.
It provides a simple command-line interface(v1)/GUI(v2) to add, edit, view, update rank information and launch accounts :)

## v2 Prerequisites

Before using Valouncher v2, ensure that you have the following software/packages installed on your system:

- Python 3.x
- tkinter
- pyautogui
- requests
- pywinauto

## v1 Prerequisites

Before using Valouncher v1, ensure that you have the following software/packages installed on your system:

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

## WHY IS FETCH NOT WORKING FOR ME?

This feature is only currently supported in ap region for now, if you wish to use it on other region accounts edit the fetch_account_details() function's variable api_base_url to reflect your region!
```
api_base_url = 'https://api.henrikdev.xyz/valorant/v1/mmr/ap/'
```
to 
```
api_base_url = 'https://api.henrikdev.xyz/valorant/v1/mmr/{YOUR_REGION}/'
```

## Future Plans

- Add option to store accounts based on region(Next on my list as I love playing with different cultures so I have an EU and a NA account too!
- Add progress bar when fetching details for accounts ;)
- Open to suggestions :D

## Credits

Credits to [Henrik-3](https://github.com/Henrik-3/unofficial-valorant-api) for sharing a Valorant API with us!
https://github.com/Henrik-3/unofficial-valorant-api

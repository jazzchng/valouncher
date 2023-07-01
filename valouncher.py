import configparser
import ctypes
import getpass
import os
import re
import requests
import subprocess
import sys
import time
from pywinauto import Desktop
import pyautogui
import pywinauto
import win32con
import win32gui
import codecs
from tabulate import tabulate
from tqdm import tqdm

# Set the root directory path
root_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
loop = 0

# Load accounts.cfg
config_file_path = os.path.join(root_directory, 'accounts.cfg')
config = configparser.ConfigParser()

# Create the config file with UTF-8 encoding
def create_config_file():
    with open(config_file_path, 'w', encoding='utf-8') as config_file:
        config.write(config_file)

# Open the config file with UTF-8 encoding
def read_config_file():
    with codecs.open(config_file_path, 'r', encoding='utf-8') as config_file:
        config.read_file(config_file)

if not os.path.isfile(config_file_path):
    create_config_file()
else:
    read_config_file()

riot_path = r'C:\Riot Games\Riot Client\RiotClientServices.exe --launch-product=valorant --launch-patchline=live'

# Get the username
winuser = getpass.getuser()

# Create the full file path with the username
file_path = os.path.join(rf'C:\Users\{winuser}', 'AppData\Local\Riot Games\Riot Client\Data\RiotGamesPrivateSettings.yaml')

# Check if file exists and delete it
if os.path.exists(file_path):
    os.remove(file_path)

# Check if process is running and terminate it
process_name = 'VALORANT-WIN64-SHIPPING.exe'
output = subprocess.run(['tasklist', '/FI', f'imagename eq {process_name}'], capture_output=True, text=True)
if ':' not in output.stdout:
    subprocess.run(['taskkill', '/F', '/IM', process_name])

# Check if process is running and terminate it
process_name = 'RiotClientServices.exe'
output = subprocess.run(['tasklist', '/FI', f'imagename eq {process_name}'], capture_output=True, text=True)
if ':' not in output.stdout:
    subprocess.run(['taskkill', '/F', '/IM', process_name])

print(120*"=")
header = '''Welcome to Valouncher!
Version: 1.2
By Jazz Chng

==========
DISCLAIMER
==========
This is a simple Valorant Launcher that stores your username and password in an accounts.cfg file.
Passwords are stored on your local drive and NOT ENCRYPTED! USE AT YOUR OWN RISK!!
I will not be held liable for any account lost with the usage of valouncher.
Always use 2FA on your account! :D

Open source on GitHub: https://github.com/jazzchng/valouncher/
'''

print(header)
print(120*"=")

def launch_account():
    account_count = list_accounts()
    account_choice = input("Enter the account number you wish to launch (0 to go back): ")
    try:
        account_choice = int(account_choice)
        if account_choice == 0:
            return
        elif 1 <= account_choice <= account_count:
            section_name = f'account{account_choice}'
            username = config[section_name]['username']
            password = config[section_name]['password']
            print(f"Launching Account: {username}")

            # Launch RiotClientServices.exe
            subprocess.Popen(riot_path)

            # Detecting Riot Client Main window
            if wait_for_window("Riot Client Main"):
                # The window is visible and launched, continue with your code here
                while True:
                    try:
                        main_window = Desktop(backend="uia").window(title="Riot Client Main")
                        if main_window.exists():
                            # Extract and input the username and password fields
                            print(f'Credentials for: {username}')
                            username_field = main_window.child_window(title="USERNAME", auto_id="username", control_type="Edit")
                            username_field.set_text(username)
                            password_field = main_window.child_window(title="PASSWORD", auto_id="password", control_type="Edit")
                            password_field.set_text(password)

                            # Click the "Sign in" button
                            sign_in_button = main_window.child_window(title="Sign in", control_type="Button")
                            sign_in_button.click()

                            sys.exit()
                    except Exception as e:
                        clear_console()
                        print(40*"=")
                        print('Exception as e')
                        print(40*"=")
                        pass

            else:
                # Timeout occurred, handle the situation accordingly
                clear_console()
                print(40*"=")
                print("Timeout: [Riot Client Main] window not found.")
                print(40*"=")
                return
        else:
            clear_console()
            print(40*"=")
            print("Invalid account number.")
            print(40*"=")
    except ValueError:
        clear_console()
        print(40*"=")
        print("Invalid input. Please enter a number.")
        print(40*"=")

def add_account():
    section_name = f'account{len(config.sections()) + 1}'
    insert_cfg(section_name)

    clear_console()
    print(40 * "=")
    print("Account stored successfully!")
    print(40 * "=")

def edit_account():
    list_accounts()
    account_choice = int(input("Enter the account you wish to edit (0 to go back): "))
    section_name = f"account{account_choice}"

    if account_choice == 0:
        clear_console()
        return

    
    if section_name not in config.sections():
        clear_console()
        print(40 * "=")
        print(f"Account with index {account_choice} does not exist.")
        print(40 * "=")
        return

    account_data = config[section_name]
    username = account_data.get('username')

    print(f"Editing Account - {section_name[7:]}. {username}")

    insert_cfg(section_name)

    clear_console()
    print(40 * "=")
    print("Account updated successfully!")
    print(40 * "=")

def insert_cfg(section_name):
    while True:
        username = input("Enter username: ")
        if re.match("^[a-zA-Z0-9]+$", username):
            break
        else:
            print("Username can only contain letters and numbers. Please try again.")

    while True:
        password = input("Enter password: ")
        if password:
            break
        else:
            print("Password is mandatory. Please try again.")

    while True:
        player_name_tag = input("Enter account PlayerName#Tag (optional): ")
        if not player_name_tag:
            player_name = ''
            player_tag = ''
            break
        match = re.match(r"(\w+)#(\d+)", player_name_tag)
        if match:
            player_name = match.group(1)
            player_tag = match.group(2)
            break
        else:
            print("Invalid player name and tag format! Please try again. (Include the tag '#')")

    account_description = input("Enter account description (optional): ")

    config[section_name] = {
        'username': username,
        'password': password,
        'player_name': player_name,
        'player_tag': player_tag,
        'currenttier': '',
        'currenttierpatched': '',
        'ranking_in_tier': '',
        'mmr_change_to_last_game': '',
        'elo': ''
    }

    if account_description:
        config[section_name]['account_description'] = account_description

    create_config_file()

def view_accounts():
    account_count = list_accounts()
    while True:
        account_choice = input("Enter the account number you wish to view details (0 to go back): ")
        if account_choice == '0':
            clear_console()
            return
        elif account_choice.isdigit():
            account_choice = int(account_choice)
            if 1 <= account_choice <= account_count:
                section_name = f"account{account_choice}"
                account_data = config[section_name]
                clear_console()
                print(40 * "=")
                print(f"Account Details - {section_name[7:]}. {account_data.get('username', '')}")
                print(40 * "=")
                print(f"                IGN: {account_data.get('player_name', '')}#{account_data.get('player_tag', '')}")
                print(f"       Current Rank: {account_data.get('currenttierpatched', '')}")
                print(f"                 RR: {account_data.get('ranking_in_tier', '')}")
                print(f"  RR From Last Game: {account_data.get('mmr_change_to_last_game', '')}")
                print(f"                Elo: {account_data.get('elo', '')}")
                print(f"       Current Tier: {account_data.get('currenttier', '')}")
                print(f"Account Description: {account_data.get('account_description', '')}")
                return
        clear_console()
        print(40 * "=")
        print("Invalid choice. Please try again.")
        print(40 * "=")

def list_accounts():
    read_config_file()
    if not os.path.isfile(config_file_path):
        clear_console()
        print(40 * "=")
        print("No accounts found.")
        print(40 * "=")
        return 0, None, None  # Return default values if no accounts found

    account_count = len(config.sections())
    if account_count == 0:
        clear_console()
        print(40 * "=")
        print("No accounts found.")
        print(40 * "=")
        return 0, None, None  # Return default values if no accounts found

    table_data = []
    for i, section_name in enumerate(config.sections(), start=1):
        account_data = config[section_name]
        username = account_data['username']
        ign = f"{account_data['player_name']}#{account_data['player_tag']}"
        rank = account_data['currenttierpatched']
        rr = account_data['ranking_in_tier']
        if rank == '':
            printrank = 'NO RANK STORED'
        else:
            printrank = f"{rank} ({rr}/100)"
        
        if username is not None:
            if ign == '#':
                table_data.append([i, username])
            else:
                table_data.append([i, username, ign, printrank])

    table_headers = ["#", "Account", "IGN#TAG", "Rank (RR)    "]
    table = tabulate(table_data, headers=table_headers, tablefmt="fancy_grid", colalign=("right", "center", "center", "right"))
    
    clear_console()
    print(120 * "=")
    print("Select account:")
    print(120 * "=")
    print(table)
    print("0. Go back to the main menu")
    print(120 * "=")
    
    return account_count

def wait_for_window(window_title, timeout=60):
    start_time = time.time()
    while time.time() - start_time < timeout:
        if pyautogui.getWindowsWithTitle(window_title):
            return True
        time.sleep(1)
    return False

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def fetch_account_details():
    api_base_url = 'https://api.henrikdev.xyz/valorant/v1/mmr/ap/'

    # Get the total number of accounts
    total_accounts = len(config.sections())

    # Use tqdm to create a progress bar
    with tqdm(total=total_accounts, ncols=100) as pbar:
        # List all accounts
        for i, section_name in enumerate(config.sections(), start=1):
            account_data = config[section_name]
            username = account_data['username']
            player_name = account_data['player_name']
            player_tag = account_data['player_tag']

            if not player_name or not player_tag:
                tqdm.write(f"No   IGN   Stored  for {i}. Skipping account: {username}")
                pbar.update(1)  # Update the progress bar
                continue

            # Encode the player name and tag for the API request
            encoded_player_name = requests.utils.quote(player_name)
            encoded_player_tag = requests.utils.quote(player_tag)
            api_url = f'{api_base_url}{encoded_player_name}/{encoded_player_tag}'

            try:
                response = requests.get(api_url)
                response.raise_for_status()  # Check for any errors in the response

                # Parse the API response and retrieve the player information
                player_info = response.json()['data']

                # Update the configuration with the player information
                config[section_name]['currenttier'] = str(player_info.get('currenttier', ''))
                config[section_name]['currenttierpatched'] = player_info.get('currenttierpatched', '')
                config[section_name]['ranking_in_tier'] = str(player_info.get('ranking_in_tier', ''))
                config[section_name]['mmr_change_to_last_game'] = str(player_info.get('mmr_change_to_last_game', ''))
                config[section_name]['elo'] = str(player_info.get('elo', ''))

                create_config_file()

                tqdm.write(f"Player information for {i}. {player_name}#{player_tag} (Account: {username}) retrieved and stored successfully!")
            except requests.exceptions.RequestException as e:
                tqdm.write(f"Failed to retrieve player information for {player_name}#{player_tag} (Account: {username}): {str(e)}")

            pbar.update(1)  # Update the progress bar

        tqdm.write(120 * "=")
        tqdm.write("Account details fetched for all stored accounts.")
        tqdm.write(120 * "=")

# Main loop
while True:
    if loop == 0:
        print(40*"=")
        print("How may I help you today? :D")
        print(40*"=")
    else:
        print(40*"=")
        print("What can I do for you next? :D")
        print(40*"=")
    print("1. Launch Account")
    print("2. Add Account")
    print("3. Edit Account")
    print("4. View Stored Accounts")
    print("5. Fetch Account Details")
    print("0. Exit")
    
    read_config_file()
    choice = input("Enter your choice: ")
    
    loop += 1
    
    if choice == '1':
        launch_account()
    elif choice == '2':
        add_account()
    elif choice == '3':
        edit_account()
    elif choice == '4':
        view_accounts()
    elif choice == '5':
        fetch_account_details()
    elif choice == '0':
        break
    else:
        clear_console()
        print(40*"=")
        print("Invalid choice. Please try again.")
        print(40*"=")

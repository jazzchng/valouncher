import os
import configparser
import subprocess
import re
import time
import win32gui
import win32con
import pyautogui
import pywinauto
from pywinauto import Desktop
import sys
import ctypes

# Specify the full path to the file
file_path = r'C:\Users\Jazz\AppData\Local\Riot Games\Riot Client\Data\RiotGamesPrivateSettings.yaml'

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

# Set the root directory path
root_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
loop = 0

print(120*"=")
header = '''
Welcome to Valouncher!
Version: 1.0
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

def store_account():
    config_file_path = os.path.join(root_directory, 'accounts.cfg')

    if not os.path.isfile(config_file_path):
        create_config_file()

    config = configparser.ConfigParser()
    config.read(config_file_path)
    
    username = input("Enter username: ")
    password = input("Enter password: ")
    
    section_name = f'account{len(config.sections())}'
    config[section_name] = {'username': username, 'password': password}
    
    with open(config_file_path, 'w') as config_file:
        config.write(config_file)
    
    clear_console()
    print(40*"=")
    print("Account stored successfully!")
    print(40*"=")

def launch_account():
    config_file_path = os.path.join(root_directory, 'accounts.cfg')

    if not os.path.isfile(config_file_path):
        clear_console()
        print(40*"=")
        print("No accounts found. Please add an account.")
        print(40*"=")
        return

    config = configparser.ConfigParser()
    config.read(config_file_path)

    account_count = len(config.sections())
    if account_count == 0:
        clear_console()
        print(40*"=")
        print("No accounts found. Please add an account.")
        print(40*"=")
        return
    
    clear_console()
    print(40*"=")
    print("Stored accounts:")
    for i in range(1, account_count):
        section_name = f'account{i}'
        username = config[section_name]['username']
        password = config[section_name]['password']

        print(f"{i}. {username}")
    print(40*"=")

    account_choice = input("Enter the account number to launch (or '0' to go back): ")
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
            subprocess.Popen(r'C:\Riot Games\Riot Client\RiotClientServices.exe')

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

def view_accounts():
    config_file_path = os.path.join(root_directory, 'accounts.cfg')

    if not os.path.isfile(config_file_path):
        clear_console()
        print(40*"=")
        print("No accounts found.")
        print(40*"=")
        return

    config = configparser.ConfigParser()
    config.read(config_file_path)

    account_count = len(config.sections())
    if account_count == 0:
        clear_console()
        print(40*"=")
        print("No accounts found.")
        print(40*"=")
        return

    clear_console()
    print(40*"=")
    print("Currently stored accounts:")

    for i in range(1, account_count):
        section_name = f'account{i}'
        username = config[section_name]['username']
        password = config[section_name]['password']

        print(f"{i}. {username}")
    print(40*"=")

def wait_for_window(window_title, timeout=60):
    start_time = time.time()
    while time.time() - start_time < timeout:
        if pyautogui.getWindowsWithTitle(window_title):
            return True
        time.sleep(1)
    return False

# Function to clear the console
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

# Set the console window size
def set_console_window_size(width, height):
    try:
        # Get the handle of the console window
        console_handle = ctypes.windll.kernel32.GetConsoleWindow()

        # Set the console window size
        ctypes.windll.kernel32.SetWindowPos(console_handle, 0, 0, 0, width, height, 0x0002 | 0x0040)
    except Exception as e:
        print('An error occurred while setting the console window size:', str(e))

def create_config_file():
    config = configparser.ConfigParser()
    config.add_section('accounts')

    config_file_path = os.path.join(root_directory, 'accounts.cfg')
    with open(config_file_path, 'w') as config_file:
        config.write(config_file)

# Main loop
while True:
    if loop == 0:
        print(40*"=")
        print("How may I help you today? :D")
        print(40*"=")
    else:
        print("What can I do for you next? :D")
    print("1. Launch Account")
    print("2. Add Account")
    print("3. View Stored Accounts")
    print("0. Exit")
    
    choice = input("Enter your choice: ")
    loop +=1
    
    if choice == '1':
        launch_account()
    elif choice == '2':
        store_account()
    elif choice == '3':
        view_accounts()
    elif choice == '0':
        break
    else:
        clear_console()
        print(40*"=")
        print("Invalid choice. Please try again.")
        print(40*"=")